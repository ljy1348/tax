from src.models import TaxReturnData, TaxReturnHeader, TaxWithholdingSummary


def get_sample_data() -> TaxReturnData:
    """
    data/예시 데이터.txt 내용을 바탕으로 생성한 샘플 데이터
    """

    # Header Data
    header = TaxReturnHeader(
        taxpayer_id="1234567891",  # 입력!!!
        attribution_year_month="202512",  # 입력!!!
        payment_year_month="202512",  # 입력!!!
        submission_year_month="202501",  # 입력!!!
        user_id="chars",  # 입력!!!
        company_name="대한상회",  # 입력!!!
        representative_name="김철수",  # 입력!!!
        write_date="20260110",  # 오늘 -> 임의 지정 (신고일: 2026년 01월 10일)
        program_code="9000",  # 입력!!!
    )

    # Summary Data
    summaries = []

    # 1. A25 (매월 사업소득)
    # 인원 1, 총지급액 1,000,000, 소득세 30,000
    s1 = TaxWithholdingSummary(
        income_code="A25",
        count=1,
        total_payment=1000000,
        collected_tax=30000,
        collected_rural_tax=0,
        penalty_tax=0,
        adjusted_refund_tax=0,
        paid_tax=30000,  # 납부세액(소득세 등)
        paid_rural_tax=0,
    )
    summaries.append(s1)

    # 2. A30 (사업소득 가감계 - 예시 데이터 txt에 A30도 있음)
    # 인원 1, 총지급액 1,000,000, 소득세 30,000
    s2 = TaxWithholdingSummary(
        income_code="A30",
        count=1,
        total_payment=1000000,
        collected_tax=30000,
        collected_rural_tax=0,
        penalty_tax=0,
        adjusted_refund_tax=0,
        paid_tax=30000,
        paid_rural_tax=0,
    )
    summaries.append(s2)

    return TaxReturnData(header=header, summaries=summaries)
