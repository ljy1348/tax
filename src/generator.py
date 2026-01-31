from src.models import TaxReturnData, TaxReturnHeader, TaxWithholdingSummary


class TaxReturnGenerator:
    """
    원천세 전자신고 파일 생성기
    Encoding: EUC-KR (CP949)
    """

    ENCODING = "cp949"

    def generate(self, data: TaxReturnData) -> bytes:
        parts = []

        # 1. Header Record
        header_bytes = self._create_header(data.header)
        if len(header_bytes) != 400:
            raise ValueError(
                f"Header length mismatch: expected 400, got {len(header_bytes)}"
            )
        parts.append(header_bytes)

        # 2. Data Records
        for summary in data.summaries:
            record_bytes = self._create_data_record(summary)
            if len(record_bytes) != 150:
                raise ValueError(
                    f"Data record length mismatch: expected 150, got {len(record_bytes)}"
                )
            parts.append(record_bytes)

        # Join with CRLF
        # 스펙: "LINE SEQUENTIAL (각 레코드마다 CR/LF값 삽입)"
        # 마지막 레코드 뒤에도 CRLF가 있어야 하는지, 없어야 하는지 시스템마다 다름.
        # "오류: 레코드 길이"가 뜨는 경우, 보통 마지막 빈 줄을 레코드로 인식해서 발생함.
        # 따라서 마지막 CRLF를 제거하고 연결만 함.
        return b"\r\n".join(parts)

    def _create_header(self, h: TaxReturnHeader) -> bytes:
        """
        원천징수이행상황신고서_Header (Length: 400)
        """
        b = b""
        b += self._fmt_str(h.data_type, 2)
        b += self._fmt_str(h.form_code, 7)
        b += self._fmt_str(h.taxpayer_id, 13)
        b += self._fmt_str(h.tax_item_code, 2)
        b += self._fmt_str(h.report_type, 2)
        b += self._fmt_str(h.report_detail_type, 2)
        b += self._fmt_str(h.report_kind_code, 3)
        b += self._fmt_str(h.attribution_year_month, 6)
        b += self._fmt_str(h.payment_year_month, 6)
        b += self._fmt_str(h.submission_year_month, 6)
        b += self._fmt_str(h.user_id, 20)
        b += self._fmt_str("FF001", 5)  # 민원종류코드 (Default)
        b += self._fmt_str("", 10)  # 세무대리인 사업자번호
        b += self._fmt_str("", 30)  # 세무대리인 성명
        b += self._fmt_str("", 6)  # 세무대리인 관리번호
        b += self._fmt_str("", 14)  # 세무대리인 전화번호
        b += self._fmt_str(h.company_name, 30)
        b += self._fmt_str("", 70)  # 사업장소재지
        b += self._fmt_str("", 14)  # 사업장전화번호
        b += self._fmt_str("", 50)  # 전자메일주소
        b += self._fmt_str(h.representative_name, 30)
        b += self._fmt_str("01", 2)  # 원천신고구분 (01: 매월) - 일단 고정
        b += self._fmt_str(h.year_end_settlement_yn, 1)
        b += self._fmt_str(h.income_disposition_yn, 1)
        b += self._fmt_str(h.refund_application_yn, 1)
        b += self._fmt_str(h.batch_payment_yn, 1)
        b += self._fmt_str(h.biz_unit_tax_yn, 1)
        b += self._fmt_str(h.sub_sheet_yn, 1)
        b += self._fmt_str(h.carry_over_refund_yn, 1)
        b += self._fmt_str(h.pre_payment_yn, 1)
        b += self._fmt_str("", 3)  # 예입처
        b += self._fmt_str("", 20)  # 계좌번호
        b += self._fmt_str(h.write_date, 8)
        b += self._fmt_str(h.program_code, 4)
        b += self._fmt_str("", 27)  # 공란

        return b

    def _create_data_record(self, s: TaxWithholdingSummary) -> bytes:
        """
        원천징수이행상황신고서_원천징수 명세 및 납부세액 (Length: 150)
        """
        b = b""
        b += self._fmt_str(s.data_type, 2)
        b += self._fmt_str(s.form_code, 7)
        b += self._fmt_str(s.income_code, 3)
        b += self._fmt_num(s.count, 15)
        b += self._fmt_num(s.total_payment, 15)
        b += self._fmt_num(s.collected_tax, 15)
        b += self._fmt_num(s.collected_rural_tax, 15)
        b += self._fmt_num(s.penalty_tax, 15)
        b += self._fmt_num(s.adjusted_refund_tax, 15)
        b += self._fmt_num(s.paid_tax, 15)
        b += self._fmt_num(s.paid_rural_tax, 15)
        b += self._fmt_str("", 18)  # 공란

        return b

    def _fmt_str(self, val: str, length: int) -> bytes:
        """문자열 포맷팅: Left align, Space padding (Byte length 기준)"""
        encoded_val = val.encode(self.ENCODING)
        if len(encoded_val) > length:
            # Truncate (한글 깨짐 주의해야 하지만 여기서는 단순 Truncate)
            # 안전하게 하려면 길이를 체크해서 잘라야 함
            return encoded_val[:length]

        padding = b" " * (length - len(encoded_val))
        return encoded_val + padding

    def _fmt_num(self, val: int, length: int) -> bytes:
        """숫자 포맷팅: Right align, Zero padding"""
        s_val = str(val)
        # 음수 처리
        if val < 0:
            # "-00100" 형태 (스펙 확인 필요, 보통 길이에 포함됨)
            # "길이가 6자리인 경우 음수 100은 -00100"
            # 부호 포함하여 length 자리를 맞춰야 함.
            # Python zfill은 "-00100"을 만들어줌 but custom logic needed to be sure.
            s_val = f"{val:0{length}d}"  # -0000000000100
        else:
            s_val = f"{val:0{length}d}"

        encoded_val = s_val.encode(self.ENCODING)
        if len(encoded_val) > length:
            raise ValueError(f"Number {val} too long for field length {length}")
        return encoded_val
