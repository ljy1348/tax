from src.models import (
    TaxReturnData,
    TaxReturnHeader,
    TaxWithholdingSummary,
    YearMonth,
    YMD,
    NonNegativeInt,
)


def get_sample_data() -> TaxReturnData:
    """
    data/예시 데이터.txt 내용을 바탕으로 생성한 샘플 데이터
    """

    # Header Data
    header = TaxReturnHeader(
        corp_no="1234567891",  # 납세자ID
        attribution_year_month=YearMonth("202512"),
        payment_year_month=YearMonth("202512"),
        submission_year_month=YearMonth("202601"),
        hometax_id="chars",  # 사용자ID
        corp_name="대한상회",  # 법인명(상호)
        representative_name="김철수",
        write_date=YMD("20260110"),  # 오늘 -> 임의 지정 (신고일: 2026년 01월 10일)
        program_code="9000",
    )

    # Summary Data
    summaries = []

    # 1. A25 (매월 사업소득)
    # 인원 1, 총지급액 1,000,000, 소득세 30,000
    s1 = TaxWithholdingSummary(
        income_code="A25",
        count=NonNegativeInt(1),
        total_payment=NonNegativeInt(1000000),
        collected_tax=NonNegativeInt(30000),
        collected_rural_tax=NonNegativeInt(0),
        penalty_tax=NonNegativeInt(0),
        adjusted_refund_tax=0,  # int
        paid_tax=NonNegativeInt(30000),  # 납부세액(소득세 등)
        paid_rural_tax=NonNegativeInt(0),
    )
    summaries.append(s1)

    # 2. A30 (사업소득 가감계 - 예시 데이터 txt에 A30도 있음)
    # 인원 1, 총지급액 1,000,000, 소득세 30,000
    s2 = TaxWithholdingSummary(
        income_code="A30",
        count=NonNegativeInt(1),
        total_payment=NonNegativeInt(1000000),
        collected_tax=NonNegativeInt(30000),
        collected_rural_tax=NonNegativeInt(0),
        penalty_tax=NonNegativeInt(0),
        adjusted_refund_tax=0,  # int
        paid_tax=NonNegativeInt(30000),
        paid_rural_tax=NonNegativeInt(0),
    )
    summaries.append(s2)

    return TaxReturnData(header=header, summaries=summaries)
