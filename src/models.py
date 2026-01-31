from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TaxReturnHeader:
    """원천징수이행상황신고서 Header Record (C103900)"""

    # 필수 항목
    taxpayer_id: str  # 납세자ID (사업자번호)
    attribution_year_month: str  # 귀속연월 (YYYYMM)
    payment_year_month: str  # 지급연월 (YYYYMM)
    submission_year_month: str  # 제출연월 (YYYYMM)
    user_id: str  # 사용자ID
    company_name: str  # 법인명(상호)
    representative_name: str  # 성명(대표자명)
    write_date: str  # 작성일자 (YYYYMMDD)

    # 선택/기본값 항목
    data_type: str = "21"  # 자료구분
    form_code: str = "C103900"  # 서식코드
    tax_item_code: str = "14"  # 세목코드
    report_type: str = "01"  # 신고구분코드 (01: 정기)
    report_detail_type: str = "01"  # 신고구분상세코드 (01: 정기)
    report_kind_code: str = "F01"  # 신고서종류코드

    # 여부 플래그 (Default N)
    year_end_settlement_yn: str = "N"  # 연말정산여부
    income_disposition_yn: str = "N"  # 소득처분여부
    refund_application_yn: str = "N"  # 환급신청여부
    batch_payment_yn: str = "N"  # 일괄납부여부
    biz_unit_tax_yn: str = "N"  # 사업자단위과세여부
    sub_sheet_yn: str = "N"  # 신고서부표여부
    carry_over_refund_yn: str = "N"  # 차월이월환급세액 승계명세여부
    pre_payment_yn: str = "N"  # 기납부세액명세서 제출여부

    program_code: str = "9000"  # 세무프로그램코드


@dataclass
class TaxWithholdingSummary:
    """원천징수이행상황신고서 Data Record (C103900 - 원천징수 명세 및 납부세액)"""

    income_code: str  # 원천징수소득코드 (예: A25)

    count: int = 0  # 인원
    total_payment: int = 0  # 총지급액
    collected_tax: int = 0  # 징수세액(소득세 등)
    collected_rural_tax: int = 0  # 징수세액(농특세)
    penalty_tax: int = 0  # 가산세
    adjusted_refund_tax: int = 0  # 당월조정환급세액
    paid_tax: int = 0  # 납부세액(소득세 등)
    paid_rural_tax: int = 0  # 납부세액(농특세)

    data_type: str = "23"  # 자료구분
    form_code: str = "C103900"  # 서식코드


@dataclass
class TaxReturnData:
    """전체 신고서 데이터"""

    header: TaxReturnHeader
    summaries: List[TaxWithholdingSummary]
