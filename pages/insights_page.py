
from html import escape

import streamlit as st

from analytics.competitors import get_weekly_insights


st.markdown('''
<style>
    .insights-hero {
        background: #E5E9D9;
        border: 1px solid #D9E0CB;
        border-radius: 24px;
        padding: 32px 36px;
        margin-bottom: 28px;
    }

    .insights-hero-label {
        color: #69764F;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .insights-hero h1 {
        color: #30372F;
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin: 0 0 12px 0;
        padding: 0;
    }

    .insights-hero p {
        color: #58614E;
        font-size: 16px;
        margin: 0;
    }

    .insights-section {
        margin-top: 28px;
        margin-bottom: 18px;
    }

    .insights-section-label {
        color: #838F58;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .insights-section h2 {
        font-size: 28px;
        color: #30372F;
        letter-spacing: -0.03em;
        margin: 0;
    }

    .insights-section p {
        color: #7A7D72;
        font-size: 14px;
        margin-top: 8px;
    }

    .insight-card {
        border-radius: 16px;
        padding: 20px 24px;
        margin: 14px 0 20px;
        color: #30372F;
        line-height: 1.65;
    }

    .insight-card h3 {
        font-size: 17px;
        font-weight: 650;
        margin: 0 0 10px;
        color: #30372F;
    }

    .insight-card p {
        font-size: 15px;
        margin: 0;
    }

    .insight-warning {
        background: #F5E5E8;
        border-left: 3px solid #D7A6B1;
    }

    .insight-success, .insight-info {
        background: #E8EDDF;
        border-left: 3px solid #838F58;
    }
</style>
''',unsafe_allow_html=True)


st.markdown('''
<div class="insights-hero">
    <div class="insights-hero-label">PADELOOK / АНАЛИТИКА</div>
    <h1>Аналитические выводы</h1>
    <p>Автоматическая интерпретация изменений конкурентов.</p>
</div>
''',unsafe_allow_html=True)


st.markdown('''
<div class="insights-section">
    <div class="insights-section-label">01 / ИНСАЙТЫ</div>
    <h2>Аналитический вывод недели</h2>
    <p>Автоматическая интерпретация обнаруженных изменений.</p>
</div>
''',unsafe_allow_html=True)


insights=get_weekly_insights()

for insight in insights:
    if insight['level']=='warning':
        card_type='insight-warning'
    elif insight['level']=='success':
        card_type='insight-success'
    else:
        card_type='insight-info'

    title=escape(str(insight['title']))
    description=escape(str(insight['text']))

    st.markdown(
        f'<div class="insight-card {card_type}">'
        f'<h3>{title}</h3>'
        f'<p>{description}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

st.divider()

