import streamlit as st
st.set_page_config(
    page_title='padelook',
    page_icon='🎾',
    layout='wide'
)

st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded&display=block');
    html, body, [data-testid="stApp"],
    [data-testid="stSidebar"] {
        font-family: 'Nunito Sans', sans-serif !important;
    }

    [data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] * {
    font-family: 'Nunito Sans', sans-serif !important;
}

[data-testid="stSidebarNav"] a {
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: -0.3px;
}

    [data-testid="stSidebarNav"] [aria-current="page"] {
        font-weight: 700 !important;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em;
    }

    h2, h3 {
        font-weight: 650 !important;
        letter-spacing: -0.02em;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #E9E5DB;
    }

    [data-testid="stSidebarNav"] {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebarNav"]::before {
        content: "padelook";
        display: block;
        font-family: 'Nunito Sans', sans-serif;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #48533E;
        padding: 0 16px 24px 16px;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E9E5DB;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(48, 53, 43, 0.035);
    }

    [data-testid="stMetric"]:hover {
        border-color: #D8C5CA;
        box-shadow: 0 6px 18px rgba(48, 53, 43, 0.07);
        transition: all 0.2s ease;
    }

    [data-testid="stMetricValue"] {
        font-weight: 650;
        letter-spacing: -0.03em;
    }

    [data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E9E5DB;
        border-radius: 14px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    div.stButton > button {
        border-radius: 12px;
    }
    /* Навигация padelook */

[data-testid="stSidebarNav"] ul {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

[data-testid="stSidebarNav"] a {
    min-height: 52px;
    padding: 12px 16px !important;
    border-radius: 14px;
}

[data-testid="stSidebarNav"] a p {
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 19px !important;
    font-weight: 750 !important;
    line-height: 1.4 !important;
    letter-spacing: -0.5px !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] p {
    font-weight: 800 !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #E0E5D4;
}
/* Восстанавливаем шрифт иконок Material Symbols */

[data-testid="stSidebarNav"] .material-symbols-rounded,
[data-testid="stSidebarNav"] .material-symbols-outlined,
[data-testid="stSidebarNav"] .material-icons,
[data-testid="stSidebarNav"] [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    white-space: nowrap;
    flex-shrink: 0;
}


/* 3D-декор боковой панели */

[data-testid="stSidebarContent"] {
    position: relative;
    padding-bottom: 300px;
}

[data-testid="stSidebarContent"]::after {
    content: "";
    position: absolute;
    bottom: 20px;
    left: 50%;
    width: 310px;
    height: 310px;
    transform: translateX(-50%);
    background-image: url("app/static/padelook_sidebar_decor.png");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    pointer-events: none;
    animation: padelookFloat 6s ease-in-out infinite;
}

@keyframes padelookFloat {
    0%, 100% {
        transform: translateX(-50%) translateY(0);
    }

    50% {
        transform: translateX(-50%) translateY(-12px);
    }
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebarContent"]::after {
        animation: none;
    }
}

/* Мягкие тени и объём */

[data-testid="stMetric"] {
    box-shadow: 0 10px 28px rgba(65, 72, 54, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 36px rgba(65, 72, 54, 0.13);
}

[data-testid="stExpander"] {
    box-shadow: 0 6px 20px rgba(65, 72, 54, 0.05);
    transition: box-shadow 0.3s ease;
}

[data-testid="stExpander"]:hover {
    box-shadow: 0 12px 28px rgba(65, 72, 54, 0.09);
}

/* Объём для боковой навигации */

[data-testid="stSidebarNav"] a {
    transition: background-color 0.25s ease,
                transform 0.25s ease,
                box-shadow 0.25s ease;
}

[data-testid="stSidebarNav"] a:hover {
    transform: translateX(4px);
    box-shadow: 0 5px 16px rgba(65, 72, 54, 0.07);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    box-shadow: 0 5px 16px rgba(65, 72, 54, 0.08);
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stMetric"],
    [data-testid="stSidebarNav"] a {
        transition: none;
    }
}

/* Карточка клуба */

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
    background: #E8EDDF;
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
    background: #F5E3E7;
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
    background: #F0EBDF;
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] {
    background: #E8EDDF;
}

</style>
''',unsafe_allow_html=True)

market_page=st.Page(
    'pages/market_page.py',
    title='Обзор рынка',
    icon=':material/monitoring:',
    default=True
)

analysis_page=st.Page(
    'pages/analysis_page.py',
    title='Анализ конкурентов',
    icon=':material/leaderboard:'
)

insights_page=st.Page(
    'pages/insights_page.py',
    title='Аналитические выводы',
    icon=':material/auto_awesome:'
)

navigation=st.navigation([
    market_page,
    analysis_page,
    insights_page
])

navigation.run()