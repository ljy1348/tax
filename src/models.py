from dataclasses import dataclass, field
from typing import List, Optional
from enum import StrEnum
import re
from datetime import datetime


class IncomeCode(StrEnum):
    """원천징수소득코드"""

    SALARY = "A25"  # 급여
    BONUS = "A26"  # 상여
    RETIREMENT = "A27"  # 퇴직금
    DIRECTOR_REMUNERATION = "A28"  # 임원보수
    DIRECTOR_BONUS = "A29"  # 임원상여
    DIRECTOR_RETIREMENT = "A30"  # 임원퇴직금


class ReportDetailType(StrEnum):
    """신고구분상세코드"""

    정기 = "01"  # 정기
    수정 = "02"  # 수정
    기한후 = "03"  # 기한후


class FilingType(StrEnum):
    """신고주기"""

    MONTHLY = "monthly"  # 매월
    HALF_YEARLY = "half_yearly"  # 반기


class Flag(StrEnum):
    """여부 플래그"""

    Y = "Y"
    N = "N"


class CivilPetitionCode(StrEnum):
    """민원종류코드"""

    REGULAR = "FF001"  # 원천징수이행상황신고서(원천징수세액환급신청서), 기한후 신고서
    AMENDED = "FF101"  # 원천징수이행상황 수정신고서


class YearMonth(str):
    """YYYYMM 형식 연월 문자열"""

    def __new__(cls, value: str):
        if not re.match(r"^\d{6}$", value):
            raise ValueError("YearMonth must be in YYYYMM format")

        try:
            datetime.strptime(value, "%Y%m")
        except ValueError:
            raise ValueError(f"Invalid YearMonth: {value}")

        return super().__new__(cls, value)


class YMD(str):
    """YYYYMMDD 형식 날짜 문자열"""

    def __new__(cls, value: str):
        if not re.match(r"^\d{8}$", value):
            raise ValueError("Date must be in YYYYMMDD format")

        try:
            datetime.strptime(value, "%Y%m%d")
        except ValueError:
            raise ValueError(f"Invalid Date: {value}")

        return super().__new__(cls, value)


class PositiveInt(int):
    """양의 정수 (> 0)"""

    def __new__(cls, value):
        ival = int(value)
        if ival <= 0:
            raise ValueError(f"값은 0보다 커야 합니다: {value}")
        return super().__new__(cls, ival)


class NonNegativeInt(int):
    """음수가 아닌 정수 (>= 0)"""

    def __new__(cls, value):
        ival = int(value)
        if ival < 0:
            raise ValueError(f"값은 0 이상이어야 합니다: {value}")
        return super().__new__(cls, ival)


@dataclass
class TaxReturnHeader:
    """원천징수이행상황신고서 Header Record (C103900)"""

    # 필수 항목
    corp_no: str  # 납세자ID (사업자번호)
    attribution_year_month: YearMonth  # 귀속연월 (YYYYMM)
    payment_year_month: YearMonth  # 지급연월 (YYYYMM)
    submission_year_month: YearMonth  # 제출연월 (YYYYMM)
    hometax_id: str  # 사용자ID
    corp_name: str  # 법인명(상호)
    representative_name: str  # 성명(대표자명)
    write_date: YMD  # 작성일자 (YYYYMMDD)

    # 선택/기본값 항목
    data_type: str = "21"  # 자료구분
    form_code: str = "C103900"  # 서식코드
    tax_item_code: str = "14"  # 세목코드
    report_type: str = "01"  # 신고구분코드 (01: 정기)
    report_detail_type: ReportDetailType = (
        ReportDetailType.정기
    )  # 신고구분상세코드 (01: 정기)
    report_kind_code: str = "F01"  # 신고서종류코드
    filing_type: FilingType = (
        FilingType.MONTHLY
    )  # 원천신고구분 (매월/반기) - Header 22번 항목
    bank_code: str = ""  # 은행코드
    bank_account_number: str = ""  # 계좌번호
    hometax_corp_address: str = ""  # 홈택스 사업장소재지
    hometax_corp_phone: str = ""  # 홈택스 사업장전화번호
    hometax_corp_email: str = ""  # 홈택스 사업장이메일

    # 여부 플래그 (Default N)
    year_end_settlement_yn: Flag = Flag.N  # 연말정산여부
    income_disposition_yn: Flag = Flag.N  # 소득처분여부
    refund_application_yn: Flag = Flag.N  # 환급신청여부
    batch_payment_yn: Flag = Flag.N  # 일괄납부여부
    biz_unit_tax_yn: Flag = Flag.N  # 사업자단위과세여부
    sub_sheet_yn: Flag = Flag.N  # 신고서부표여부
    carry_over_refund_yn: Flag = Flag.N  # 차월이월환급세액 승계명세여부
    pre_payment_yn: Flag = Flag.N  # 기납부세액명세서 제출여부

    program_code: str = "9000"  # 세무프로그램코드


@dataclass
class TaxWithholdingSummary:
    """원천징수이행상황신고서 Data Record (C103900 - 원천징수 명세 및 납부세액)"""

    income_code: str  # 원천징수소득코드 (예: A25)

    count: NonNegativeInt = NonNegativeInt(0)  # 인원
    total_payment: NonNegativeInt = NonNegativeInt(0)  # 총지급액
    collected_tax: NonNegativeInt = NonNegativeInt(0)  # 징수세액(소득세 등)
    collected_rural_tax: NonNegativeInt = NonNegativeInt(0)  # 징수세액(농특세)
    penalty_tax: NonNegativeInt = NonNegativeInt(0)  # 가산세
    adjusted_refund_tax: int = 0  # 당월조정환급세액
    paid_tax: NonNegativeInt = NonNegativeInt(0)  # 납부세액(소득세 등)
    paid_rural_tax: NonNegativeInt = NonNegativeInt(0)  # 납부세액(농특세)

    data_type: str = "23"  # 자료구분
    form_code: str = "C103900"  # 서식코드


@dataclass
class TaxRefundAdjustment:
    """원천징수이행상황신고서_환급세액 조정 (C103900 - 자료구분 22)"""

    # (12) 전월미환급세액
    prev_unrefunded_tax: NonNegativeInt = NonNegativeInt(0)
    # (13) 기환급신청세액
    prev_refund_application_tax: NonNegativeInt = NonNegativeInt(0)
    # (14) 차감잔액
    deduction_balance: NonNegativeInt = NonNegativeInt(0)
    # (15) 일반환급세액
    general_refund_tax: NonNegativeInt = NonNegativeInt(0)
    # (16) 신탁재산세액
    trust_property_tax: NonNegativeInt = NonNegativeInt(0)
    # (17) 그밖의환급세액-금융회사 등
    other_refund_tax_financial: NonNegativeInt = NonNegativeInt(0)
    # (17) 그밖의환급세액-합병 등
    other_refund_tax_merger: NonNegativeInt = NonNegativeInt(0)
    # (18) 조정대상환급세액
    adjustment_target_tax: NonNegativeInt = NonNegativeInt(0)
    # (19) 당월조정환급세액계 (정수 검증)
    current_adjusted_refund_tax: int = 0
    # (20) 차월이월환급세액
    carry_over_refund_tax: NonNegativeInt = NonNegativeInt(0)
    # (21) 환급신청액
    refund_application_tax: NonNegativeInt = NonNegativeInt(0)
    # 승계대상합계 차월이월환급세액
    total_carry_over_refund_tax: NonNegativeInt = NonNegativeInt(0)

    data_type: str = "22"  # 자료구분
    form_code: str = "C103900"  # 서식코드
    blank: str = ""  # 공란


@dataclass
class TaxReturnData:
    """전체 신고서 데이터"""

    header: TaxReturnHeader
    summaries: List[TaxWithholdingSummary]
    refund_adjustment: Optional[TaxRefundAdjustment] = None


def validate_filing_dates(
    submission_ym: str,
    payment_ym: str,
    attribution_ym: str,
    report_type: ReportDetailType = ReportDetailType.정기,
    filing_type: FilingType = FilingType.MONTHLY,
    income_disposition_yn: Flag = Flag.N,
    is_deemed_payment: bool = False,
    is_closed_business: bool = False,
    closing_month: Optional[int] = None,
) -> List[str]:
    """
    제출/지급/귀속연월 유효성 검증

    Args:
        submission_ym: 제출연월 (YYYYMM)
        payment_ym: 지급연월 (YYYYMM)
        attribution_ym: 귀속연월 (YYYYMM)
        report_type: 신고구분 (정기/수정/기한후)
        filing_type: 신고주기 (매월/반기)
        income_disposition_yn: 소득처분여부 (Y/N)
        is_deemed_payment: 지급의제 여부
        is_closed_business: 폐업/반기포기 사업자 여부
        closing_month: 폐업/포기일이 속하는 월 (반기신고 폐업시 필수)

    Returns:
        에러 메시지 리스트 (비어있으면 유효함)
    """
    errors = []

    # 날짜 파싱 헬퍼
    def parse_ym(ym_str):
        if not re.match(r"^\d{6}$", ym_str):
            raise ValueError("YYYYMM 형식이어야 합니다.")
        return int(ym_str[:4]), int(ym_str[4:])

    try:
        sub_y, sub_m = parse_ym(submission_ym)
        pay_y, pay_m = parse_ym(payment_ym)
        attr_y, attr_m = parse_ym(attribution_ym)
    except ValueError:
        errors.append("날짜 형식이 올바르지 않습니다.")
        return errors

    pay_dt = datetime(pay_y, pay_m, 1)
    attr_dt = datetime(attr_y, attr_m, 1)

    # 1. 정기신고서
    if report_type == ReportDetailType.정기:
        if filing_type == FilingType.MONTHLY:
            # (1) 매월신고
            # ① 지급연월 = 제출연월 - 1
            # (단, 2015년 3월 이후 같은 달 허용 안됨 -> -1개월 규칙으로 커버됨)
            month_diff = (sub_y - pay_y) * 12 + (sub_m - pay_m)
            if month_diff != 1:
                errors.append(
                    f"정기(매월): 제출연월({submission_ym})은 지급연월({payment_ym})의 다음달이어야 합니다."
                )

            # ② 지급연월 >= 귀속연월
            if pay_dt < attr_dt:
                errors.append(
                    f"정기(매월): 지급연월({payment_ym})은 귀속연월({attribution_ym})보다 같거나 이후여야 합니다."
                )

            # ③ 소득처분 검증
            if income_disposition_yn == Flag.N and not is_deemed_payment:
                if pay_y != attr_y:
                    errors.append(
                        f"정기(매월): 소득처분이 아니고 지급의제가 아닌 경우, 지급연도({pay_y})와 귀속연도({attr_y})는 같아야 합니다."
                    )
            else:
                # 소득처분 Y 또는 지급의제
                if pay_y < attr_y:
                    errors.append(
                        f"정기(매월): 소득처분 또는 지급의제인 경우, 지급연도({pay_y})는 귀속연도({attr_y})보다 같거나 커야 합니다."
                    )

        elif filing_type == FilingType.HALF_YEARLY:
            # (2) 반기신고
            if sub_m not in [1, 7]:
                errors.append("정기(반기): 제출연월은 1월 또는 7월이어야 합니다.")
                return errors  # 더 이상 검증 불가

            is_upper_half_submission = sub_m == 7  # 7월 제출 (상반기분)
            # 1월 제출 (하반기분) -> 상반기분 제출일수도 있으나 정기신고는 1/7월 고정

            if not is_closed_business:
                # ① 계속사업자
                if is_upper_half_submission:
                    # 상반기분: 귀속 1월, 지급 6월, 제출 7월
                    if attr_m != 1:
                        errors.append("정기(반기/상반기): 귀속연월은 1월이어야 합니다.")
                    if pay_m != 6:
                        errors.append("정기(반기/상반기): 지급연월은 6월이어야 합니다.")
                    if sub_y != pay_y:
                        errors.append(
                            "정기(반기/상반기): 제출연도와 지급연도는 같아야 합니다."
                        )
                else:
                    # 하반기분: 귀속 7월, 지급 12월, 제출 다음해 1월
                    if attr_m != 7:
                        errors.append("정기(반기/하반기): 귀속연월은 7월이어야 합니다.")
                    if pay_m != 12:
                        errors.append(
                            "정기(반기/하반기): 지급연월은 12월이어야 합니다."
                        )
                    if sub_y != pay_y + 1:
                        errors.append(
                            "정기(반기/하반기): 제출연도는 지급연도의 다음해여야 합니다."
                        )
            else:
                # ② 폐업/포기 사업자
                if is_upper_half_submission:
                    # 상반기 포기: 귀속 1월, 지급 포기월, 제출 7월
                    if attr_m != 1:
                        errors.append(
                            "정기(반기/폐업/상반기): 귀속연월은 1월이어야 합니다."
                        )
                    if closing_month and pay_m != closing_month:
                        errors.append(
                            f"정기(반기/폐업/상반기): 지급연월({pay_m})은 폐업일이 속하는 월({closing_month})이어야 합니다."
                        )
                    if sub_y != pay_y:
                        errors.append(
                            "정기(반기/폐업/상반기): 제출연도와 지급연도는 같아야 합니다."
                        )
                else:
                    # 하반기 포기: 귀속 7월, 지급 포기월, 제출 다음해 1월
                    if attr_m != 7:
                        errors.append(
                            "정기(반기/폐업/하반기): 귀속연월은 7월이어야 합니다."
                        )
                    if closing_month and pay_m != closing_month:
                        errors.append(
                            f"정기(반기/폐업/하반기): 지급연월({pay_m})은 폐업일이 속하는 월({closing_month})이어야 합니다."
                        )
                    if sub_y != pay_y + 1:
                        errors.append(
                            "정기(반기/폐업/하반기): 제출연도는 지급연도의 다음해여야 합니다."
                        )

    # 2. 수정, 기한 후 신고서
    elif report_type in [ReportDetailType.수정, ReportDetailType.기한후]:
        # ① 귀속연도는 현재연도(제출연도)의 5년 전까지
        if (sub_y - attr_y) > 5:
            errors.append(
                f"수정/기한후: 귀속연도({attr_y})는 제출연도({sub_y}) 기준 5년 전까지만 설정 가능합니다."
            )

        # ② 소득처분 검증
        if income_disposition_yn == Flag.N and not is_deemed_payment:
            if pay_y != attr_y:
                errors.append(
                    f"수정/기한후: 소득처분이 아니고 지급의제가 아닌 경우, 지급연도({pay_y})와 귀속연도({attr_y})는 같아야 합니다."
                )
        else:
            # 소득처분 Y 또는 지급의제
            if pay_y < attr_y:
                errors.append(
                    f"수정/기한후: 소득처분 또는 지급의제인 경우, 지급연도({pay_y})는 귀속연도({attr_y})보다 같거나 커야 합니다."
                )

    return errors
