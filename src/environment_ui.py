import streamlit as st


def render_environment(
    environment_state,
    weather_state
):
    """
    Render the climate-responsive visual environment.

    Thermal environment controls:
        - solar intensity
        - atmospheric background
        - solar glow

    Weather state controls:
        - cloud cover
        - precipitation
        - visibility
        - storm effects
    """

    # ==================================================
    # ENVIRONMENT STATE
    # ==================================================

    mode = environment_state.mode

    intensity = float(
        environment_state.intensity
    )

    icon = environment_state.icon

    # ==================================================
    # WEATHER STATE
    # ==================================================

    cloud_cover = float(
        weather_state.cloud_cover
    )

    precipitation = float(
        weather_state.precipitation
    )

    visibility = float(
        weather_state.visibility
    )

    weather_condition = (
        weather_state.condition
    )

    is_storm = (
        weather_condition == "storm"
    )

    # ==================================================
    # SUN POSITION
    # ==================================================

    sun_top = 105
    sun_right = 105

    # ==================================================
    # LIGHT MODE BACKGROUNDS
    # ==================================================

    light_backgrounds = {

        "extreme_heat": """
        radial-gradient(
            circle at 88% 5%,
            rgba(255, 248, 180, 1.0) 0%,
            rgba(255, 220, 105, 0.82) 12%,
            rgba(255, 187, 65, 0.42) 30%,
            rgba(255, 166, 50, 0.16) 52%,
            transparent 72%
        ),
        linear-gradient(
            135deg,
            #fff9df 0%,
            #ffe6a3 45%,
            #ffbd68 100%
        )
        """,

        "warm": """
        radial-gradient(
            circle at 88% 5%,
            rgba(255, 235, 150, 0.72) 0%,
            rgba(255, 210, 105, 0.35) 25%,
            transparent 58%
        ),
        linear-gradient(
            135deg,
            #eaf8ff 0%,
            #bfe6fa 55%,
            #ffd89b 100%
        )
        """,

        "neutral": """
        linear-gradient(
            135deg,
            #f4f8fb 0%,
            #dce7ef 50%,
            #c8d5df 100%
        )
        """,

        "cool": """
        linear-gradient(
            135deg,
            #e7f2ff 0%,
            #bfd5e8 50%,
            #9db6ca 100%
        )
        """
    }

    # ==================================================
    # DARK MODE BACKGROUNDS
    # ==================================================

    dark_backgrounds = {

        "extreme_heat": """
        radial-gradient(
            circle at 88% 5%,
            rgba(255, 190, 65, 0.55) 0%,
            rgba(255, 140, 35, 0.30) 18%,
            rgba(255, 110, 25, 0.12) 40%,
            transparent 68%
        ),
        linear-gradient(
            135deg,
            #17120f 0%,
            #2b1a10 45%,
            #412317 100%
        )
        """,

        "warm": """
        radial-gradient(
            circle at 88% 5%,
            rgba(255, 190, 70, 0.30) 0%,
            rgba(255, 145, 40, 0.10) 35%,
            transparent 60%
        ),
        linear-gradient(
            135deg,
            #101b24 0%,
            #142b38 50%,
            #30271a 100%
        )
        """,

        "neutral": """
        linear-gradient(
            135deg,
            #10161d 0%,
            #17232c 50%,
            #202d36 100%
        )
        """,

        "cool": """
        linear-gradient(
            135deg,
            #0b141d 0%,
            #112534 50%,
            #173244 100%
        )
        """
    }

    light_background = light_backgrounds.get(
        mode,
        light_backgrounds["neutral"]
    )

    dark_background = dark_backgrounds.get(
        mode,
        dark_backgrounds["neutral"]
    )

    # ==================================================
    # SOLAR PARAMETERS
    # ==================================================

    solar_strength = (
        0.35
        + intensity * 0.65
    )

    halo_opacity = min(
        0.32 + intensity * 0.55,
        0.92
    )

    ray_opacity = min(
        0.10 + intensity * 0.28,
        0.38
    )

    core_opacity = min(
        0.70 + intensity * 0.30,
        1.0
    )

    core_size = (
        110
        + int(intensity * 35)
    )

    # ==================================================
    # CLOUD PARAMETERS
    # ==================================================

    cloud_opacity = min(
        cloud_cover * 0.68,
        0.68
    )

    cloud_shadow_opacity = min(
        cloud_cover * 0.24,
        0.24
    )

    # ==================================================
    # PRECIPITATION / SOLAR ATTENUATION
    # ==================================================

    weather_attenuation = min(
        precipitation * 0.55,
        0.55
    )

    cloud_attenuation = (
        cloud_cover * 0.32
    )

    effective_solar_opacity = (
        ray_opacity
        * (1.0 - weather_attenuation)
        * (1.0 - cloud_attenuation)
    )

    # ==================================================
    # VISIBILITY
    # ==================================================

    visibility_haze = (
        1.0 - visibility
    )

    # ==================================================
    # RAIN PARAMETERS
    # ==================================================

    rain_opacity = min(
        precipitation * 0.78,
        0.78
    )

    rain_wind = (
        24
        + precipitation * 18
    )

    # ==================================================
    # WEATHER-SPECIFIC ATMOSPHERIC DARKENING
    # ==================================================

    storm_darkness = (
        0.18
        if is_storm
        else 0.0
    )

    rain_darkness = (
        precipitation * 0.08
    )

    atmospheric_darkness = (
        storm_darkness
        + rain_darkness
    )

    # ==================================================
    # STORM EFFECT HTML
    #
    # IMPORTANT:
    # This is Python, so it MUST remain outside
    # the environment_html f-string.
    # ==================================================

    if is_storm:

        storm_effect_html = """
        <div class="storm-flash-glow"></div>
        <div class="storm-lightning"></div>
        """

    else:

        storm_effect_html = ""

    # ==================================================
    # COMPLETE ENVIRONMENT HTML
    # ==================================================

    environment_html = f"""
<style>

/* ==================================================
   APPLICATION BACKGROUND
   ================================================== */

.stApp {{
    background:
        {light_background}
        !important;

    transition:
        background 1.5s ease-in-out;
}}


[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stHeader"] {{
    background:
        transparent !important;
}}


/* ==================================================
   DASHBOARD LAYER
   ================================================== */

[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 20;
}}

.main .block-container {{
    position: relative;
    z-index: 20;
}}


/* ==================================================
   SIDEBAR
   ================================================== */

[data-testid="stSidebar"] {{
    position: relative;
    z-index: 50;

    backdrop-filter:
        blur(18px);

    -webkit-backdrop-filter:
        blur(18px);
}}


/* ==================================================
   SOLAR HALO
   ================================================== */

.solar-halo {{
    position: fixed;

    top:
        calc({sun_top}px - 480px);

    right:
        calc({sun_right}px - 480px);

    width: 1050px;
    height: 1050px;

    border-radius: 50%;

    pointer-events: none;

    z-index: 1;

    opacity:
        {halo_opacity *
         (1.0 - weather_attenuation)};

    background:
        radial-gradient(
            circle,

            rgba(255,249,205,0.98) 0%,

            rgba(255,225,120,0.65) 18%,

            rgba(255,190,60,0.30) 38%,

            rgba(255,160,35,0.10) 58%,

            transparent 74%
        );

    filter:
        blur(30px);

    animation:
        solarBreath 7s ease-in-out infinite;
}}


@keyframes solarBreath {{

    0% {{
        transform:
            scale(0.96);
    }}

    50% {{
        transform:
            scale(1.04);
    }}

    100% {{
        transform:
            scale(0.96);
    }}
}}


/* ==================================================
   SOLAR RAYS
   ================================================== */

.solar-rays {{
    position: fixed;

    top:
        calc({sun_top}px - 550px);

    right:
        calc({sun_right}px - 550px);

    width: 1200px;
    height: 1200px;

    border-radius: 50%;

    pointer-events: none;

    z-index: 2;

    opacity:
        {effective_solar_opacity};

    background:
        conic-gradient(
            from 200deg,

            transparent 0deg,
            rgba(255,224,130,0.75) 7deg,
            transparent 17deg,

            transparent 25deg,
            rgba(255,220,120,0.55) 32deg,
            transparent 44deg,

            transparent 54deg,
            rgba(255,230,150,0.60) 62deg,
            transparent 73deg,

            transparent 84deg,
            rgba(255,215,105,0.50) 91deg,
            transparent 104deg,

            transparent 116deg,
            rgba(255,225,125,0.65) 124deg,
            transparent 137deg,

            transparent 149deg,
            rgba(255,215,100,0.55) 156deg,
            transparent 168deg,

            transparent 181deg,
            rgba(255,230,145,0.65) 189deg,
            transparent 202deg,

            transparent 215deg,
            rgba(255,215,100,0.55) 223deg,
            transparent 235deg,

            transparent 247deg,
            rgba(255,230,145,0.60) 255deg,
            transparent 269deg,

            transparent 281deg,
            rgba(255,215,100,0.55) 288deg,
            transparent 302deg,

            transparent 315deg,
            rgba(255,230,145,0.65) 323deg,
            transparent 337deg,

            transparent 348deg,
            rgba(255,220,120,0.60) 355deg,
            transparent 360deg
        );

    filter:
        blur(7px);

    mix-blend-mode:
        soft-light;

    transform-origin:
        50% 50%;

    animation:
        rayRotation 40s linear infinite;
}}


@keyframes rayRotation {{

    from {{
        transform:
            rotate(0deg)
            scale({solar_strength});
    }}

    to {{
        transform:
            rotate(360deg)
            scale({solar_strength});
    }}
}}


/* ==================================================
   SECONDARY SOLAR FIELD
   ================================================== */

.solar-light-field {{
    position: fixed;

    top:
        calc({sun_top}px - 350px);

    right:
        calc({sun_right}px - 350px);

    width: 760px;
    height: 760px;

    border-radius: 50%;

    pointer-events: none;

    z-index: 3;

    opacity:
        {halo_opacity * 0.55 *
         (1.0 - weather_attenuation)};

    background:
        radial-gradient(
            circle,

            rgba(255,245,180,0.55) 0%,

            rgba(255,215,100,0.24) 35%,

            transparent 70%
        );

    filter:
        blur(45px);

    mix-blend-mode:
        screen;
}}


/* ==================================================
   SUN CORE
   ================================================== */

.thermal-sun-core {{
    position: fixed;

    top:
        {sun_top}px;

    right:
        {sun_right}px;

    width:
        {core_size}px;

    height:
        {core_size}px;

    border-radius: 50%;

    pointer-events: none;

    z-index: 6;

    opacity:
        {core_opacity};

    background:
        radial-gradient(
            circle at 34% 30%,

            #ffffff 0%,

            #fffde0 12%,

            #fff3a1 32%,

            #ffd33f 62%,

            #ff9d18 100%
        );

    box-shadow:

        0 0 35px
        rgba(255,250,190,1.0),

        0 0 75px
        rgba(255,225,95,0.95),

        0 0 140px
        rgba(255,190,55,0.75),

        0 0 240px
        rgba(255,160,30,0.50),

        0 0 360px
        rgba(255,140,20,0.28);

    animation:
        sunPulse 5s ease-in-out infinite;
}}


@keyframes sunPulse {{

    0% {{
        transform:
            scale(0.98);
    }}

    50% {{
        transform:
            scale(1.06);
    }}

    100% {{
        transform:
            scale(0.98);
    }}
}}


/* ==================================================
   SOLAR CONTENT WASH
   ================================================== */

.solar-content-wash {{
    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 4;

    opacity:
        {effective_solar_opacity * 0.55};

    background:
        radial-gradient(
            circle at 86% 8%,

            rgba(255,220,120,0.30) 0%,

            rgba(255,195,80,0.10) 30%,

            transparent 65%
        );

    mix-blend-mode:
        soft-light;
}}


/* ==================================================
   CLOUD ATMOSPHERE
   ================================================== */

.cloud-field {{
    position: fixed;

    top: 0;
    left: 0;

    width: 100vw;
    height: 430px;

    overflow: hidden;

    pointer-events: none;

    z-index: 7;

    opacity:
        {cloud_opacity};
}}


/* ==================================================
   CLOUD MASS
   ================================================== */

.cloud {{
    position: absolute;

    width: 520px;
    height: 145px;

    border-radius: 50%;

    pointer-events: none;

    background:

        radial-gradient(
            ellipse at 18% 58%,
            rgba(255,255,255,0.95) 0%,
            rgba(255,255,255,0.78) 22%,
            transparent 54%
        ),

        radial-gradient(
            ellipse at 39% 36%,
            rgba(255,255,255,0.98) 0%,
            rgba(247,250,252,0.86) 24%,
            transparent 56%
        ),

        radial-gradient(
            ellipse at 59% 45%,
            rgba(255,255,255,0.93) 0%,
            rgba(239,245,249,0.78) 25%,
            transparent 57%
        ),

        radial-gradient(
            ellipse at 79% 60%,
            rgba(242,247,250,0.90) 0%,
            rgba(210,222,230,0.68) 30%,
            transparent 62%
        ),

        linear-gradient(
            180deg,
            rgba(255,255,255,0.88) 0%,
            rgba(224,234,241,0.76) 55%,
            rgba(168,184,195,0.50) 100%
        );

    filter:
        blur(7px);

    box-shadow:
        0 25px 45px
        rgba(
            35,
            50,
            62,
            {cloud_shadow_opacity}
        );
}}


/* ==================================================
   CLOUD UPPER VOLUME
   ================================================== */

.cloud::before {{
    content: "";

    position: absolute;

    inset:
        -35px -30px -20px -30px;

    border-radius: 50%;

    background:

        radial-gradient(
            ellipse at 22% 55%,
            rgba(255,255,255,0.72) 0%,
            transparent 38%
        ),

        radial-gradient(
            ellipse at 44% 30%,
            rgba(255,255,255,0.78) 0%,
            transparent 42%
        ),

        radial-gradient(
            ellipse at 67% 42%,
            rgba(255,255,255,0.60) 0%,
            transparent 40%
        ),

        radial-gradient(
            ellipse at 83% 62%,
            rgba(230,238,243,0.58) 0%,
            transparent 44%
        );

    filter:
        blur(18px);

    opacity:
        0.95;
}}


/* ==================================================
   CLOUD UNDERSIDE
   ================================================== */

.cloud::after {{
    content: "";

    position: absolute;

    left: 8%;
    right: 8%;

    bottom: -12px;

    height: 65px;

    border-radius: 50%;

    background:

        radial-gradient(
            ellipse,
            rgba(83,103,117,0.22) 0%,
            rgba(120,140,153,0.12) 35%,
            transparent 72%
        );

    filter:
        blur(18px);

    opacity:
        0.75;
}}


/* ==================================================
   CLOUD POSITIONS
   ================================================== */

.cloud-one {{
    top:
        75px;

    left:
        -520px;

    width:
        680px;

    height:
        170px;

    opacity:
        0.72;

    filter:
        blur(10px);

    animation:
        realisticCloudOne
        115s
        linear
        infinite;
}}


.cloud-two {{
    top:
        125px;

    left:
        18%;

    width:
        760px;

    height:
        190px;

    opacity:
        0.58;

    filter:
        blur(8px);

    animation:
        realisticCloudTwo
        145s
        linear
        infinite;
}}


.cloud-three {{
    top:
        45px;

    left:
        54%;

    width:
        580px;

    height:
        125px;

    opacity:
        0.38;

    filter:
        blur(13px);

    animation:
        realisticCloudThree
        165s
        linear
        infinite;
}}


.cloud-four {{
    top:
        205px;

    left:
        68%;

    width:
        720px;

    height:
        180px;

    opacity:
        0.48;

    filter:
        blur(11px);

    animation:
        realisticCloudFour
        135s
        linear
        infinite;
}}


.cloud-five {{
    top:
        285px;

    left:
        -350px;

    width:
        850px;

    height:
        150px;

    opacity:
        0.30;

    filter:
        blur(15px);

    animation:
        realisticCloudFive
        180s
        linear
        infinite;
}}


/* ==================================================
   CLOUD MOTION
   ================================================== */

@keyframes realisticCloudOne {{

    from {{
        transform:
            translateX(0)
            scale(1);
    }}

    50% {{
        transform:
            translateX(48vw)
            translateY(-8px)
            scale(1.03);
    }}

    to {{
        transform:
            translateX(145vw)
            translateY(3px)
            scale(0.98);
    }}
}}


@keyframes realisticCloudTwo {{

    from {{
        transform:
            translateX(-20vw)
            scale(1);
    }}

    50% {{
        transform:
            translateX(35vw)
            translateY(6px)
            scale(1.025);
    }}

    to {{
        transform:
            translateX(125vw)
            translateY(-4px)
            scale(0.99);
    }}
}}


@keyframes realisticCloudThree {{

    from {{
        transform:
            translateX(-15vw)
            scale(1);
    }}

    50% {{
        transform:
            translateX(40vw)
            translateY(-5px)
            scale(1.04);
    }}

    to {{
        transform:
            translateX(125vw)
            translateY(4px)
            scale(0.98);
    }}
}}


@keyframes realisticCloudFour {{

    from {{
        transform:
            translateX(-20vw)
            scale(1);
    }}

    50% {{
        transform:
            translateX(35vw)
            translateY(5px)
            scale(1.025);
    }}

    to {{
        transform:
            translateX(125vw)
            translateY(-3px)
            scale(1);
    }}
}}


@keyframes realisticCloudFive {{

    from {{
        transform:
            translateX(0)
            scale(1);
    }}

    50% {{
        transform:
            translateX(55vw)
            translateY(-4px)
            scale(1.02);
    }}

    to {{
        transform:
            translateX(145vw)
            translateY(3px)
            scale(0.98);
    }}
}}


/* ==================================================
   ATMOSPHERIC HAZE
   ================================================== */

.atmospheric-haze {{
    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 8;

    background:
        rgba(
            210,
            220,
            228,
            {visibility_haze * 0.10}
        );

    backdrop-filter:
        blur({visibility_haze * 1.5}px);

    -webkit-backdrop-filter:
        blur({visibility_haze * 1.5}px);
}}


/* ==================================================
   RAIN PARTICLE FIELD
   ================================================== */

.rain-field {{
    position: fixed;

    inset: 0;

    overflow: hidden;

    pointer-events: none;

    z-index: 12;

    opacity:
        {rain_opacity};
}}


/* ==================================================
   INDIVIDUAL RAIN DROPLETS
   ================================================== */

.rain-drop {{
    position: absolute;

    top: -15vh;

    width: 1.5px;

    height: 55px;

    border-radius: 999px;

    background:
        linear-gradient(
            180deg,
            rgba(225,242,255,0.0) 0%,
            rgba(210,235,252,0.42) 22%,
            rgba(205,232,250,0.82) 72%,
            rgba(230,245,255,0.20) 100%
        );

    box-shadow:
        0 0 4px
        rgba(190,225,250,0.22);

    transform:
        rotate(8deg);

    animation:
        naturalRainFall
        var(--rain-duration)
        linear
        var(--rain-delay)
        infinite;

    opacity:
        var(--rain-opacity);
}}


/* ==================================================
   FAR RAIN DROPLETS
   ================================================== */

.rain-drop.far {{
    width:
        1px;

    height:
        34px;

    filter:
        blur(0.5px);

    opacity:
        0.28;

    background:
        linear-gradient(
            180deg,
            transparent,
            rgba(190,220,242,0.45),
            transparent
        );
}}


/* ==================================================
   FOREGROUND RAIN DROPLETS
   ================================================== */

.rain-drop.near {{
    width:
        2px;

    height:
        82px;

    filter:
        blur(0.2px);

    background:
        linear-gradient(
            180deg,
            transparent 0%,
            rgba(220,242,255,0.62) 20%,
            rgba(215,239,255,0.94) 72%,
            rgba(240,250,255,0.18) 100%
        );

    box-shadow:
        0 0 6px
        rgba(180,220,250,0.25);
}}


/* ==================================================
   NATURAL RAIN MOVEMENT
   ================================================== */

@keyframes naturalRainFall {{

    0% {{
        transform:
            translate3d(
                0,
                -15vh,
                0
            )
            rotate(8deg);
    }}

    70% {{
        transform:
            translate3d(
                {rain_wind * 0.65}px,
                72vh,
                0
            )
            rotate(8deg);
    }}

    100% {{
        transform:
            translate3d(
                {rain_wind}px,
                120vh,
                0
            )
            rotate(8deg);
    }}
}}


/* ==================================================
   RAIN GROUND HAZE
   ================================================== */

.rain-ground {{
    position: fixed;

    left: 0;
    right: 0;

    bottom: 0;

    height: 18vh;

    pointer-events: none;

    z-index: 11;

    opacity:
        {precipitation * 0.22};

    background:
        radial-gradient(
            ellipse at center bottom,
            rgba(180,215,235,0.22),
            transparent 68%
        );

    filter:
        blur(12px);
}}


/* ==================================================
   STORM LIGHTNING
   ================================================== */

.storm-lightning {{
    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 15;

    background:
        rgba(
            235,
            245,
            255,
            0.0
        );

    opacity: 0;

    mix-blend-mode:
        screen;

    animation:
        lightningFlash
        11s
        linear
        infinite;
}}


@keyframes lightningFlash {{

    0%,
    88%,
    100% {{
        opacity: 0;
    }}

    89% {{
        opacity: 0.0;
    }}

    89.3% {{
        opacity: 0.85;
    }}

    89.7% {{
        opacity: 0.08;
    }}

    90.1% {{
        opacity: 0.65;
    }}

    90.5% {{
        opacity: 0.0;
    }}

    94% {{
        opacity: 0;
    }}

    94.2% {{
        opacity: 0.35;
    }}

    94.5% {{
        opacity: 0;
    }}
}}


/* ==================================================
   STORM SKY FLASH
   ================================================== */

.storm-flash-glow {{
    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 14;

    opacity: 0;

    background:
        radial-gradient(
            ellipse at 50% 20%,
            rgba(220,240,255,0.42) 0%,
            rgba(190,220,245,0.16) 35%,
            transparent 72%
        );

    animation:
        stormSkyFlash
        11s
        linear
        infinite;
}}


@keyframes stormSkyFlash {{

    0%,
    88%,
    100% {{
        opacity: 0;
    }}

    89.3% {{
        opacity: 0.75;
    }}

    89.7% {{
        opacity: 0.08;
    }}

    90.1% {{
        opacity: 0.55;
    }}

    90.5% {{
        opacity: 0;
    }}

    94.2% {{
        opacity: 0.28;
    }}

    94.5% {{
        opacity: 0;
    }}
}}


/* ==================================================
   ATMOSPHERIC DARKENING
   ================================================== */

.weather-darkness {{
    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 5;

    background:
        rgba(
            25,
            40,
            52,
            {atmospheric_darkness}
        );
}}


/* ==================================================
   ENVIRONMENT INDICATOR
   ================================================== */

.environment-indicator {{
    position: fixed;

    top:
        72px;

    right:
        24px;

    z-index:
        999999;

    padding:
        9px 15px;

    border-radius:
        999px;

    font-family:
        sans-serif;

    font-size:
        13px;

    font-weight:
        650;

    backdrop-filter:
        blur(14px);

    -webkit-backdrop-filter:
        blur(14px);
}}


/* ==================================================
   LIGHT MODE
   ================================================== */

@media (prefers-color-scheme: light) {{

    .stApp {{
        background:
            {light_background}
            !important;
    }}

    .environment-indicator {{
        background:
            rgba(
                255,
                255,
                255,
                0.88
            );

        color:
            #17212b;

        border:
            1px solid
            rgba(
                20,
                33,
                43,
                0.08
            );

        box-shadow:
            0 4px 20px
            rgba(
                0,
                0,
                0,
                0.12
            );
    }}
}}


/* ==================================================
   DARK MODE
   ================================================== */

@media (prefers-color-scheme: dark) {{

    .stApp {{
        background:
            {dark_background}
            !important;
    }}

    .solar-rays {{
        opacity:
            {effective_solar_opacity * 0.62};
    }}

    .solar-content-wash {{
        opacity:
            {effective_solar_opacity * 0.32};
    }}

    .environment-indicator {{
        background:
            rgba(
                20,
                27,
                34,
                0.82
            );

        color:
            #f3f7fa;

        border:
            1px solid
            rgba(
                255,
                255,
                255,
                0.10
            );

        box-shadow:
            0 6px 28px
            rgba(
                0,
                0,
                0,
                0.32
            );
    }}

    /* ----------------------------------------------
       DARK CLOUD VOLUME
       ---------------------------------------------- */

    .cloud {{
        background:

            radial-gradient(
                ellipse at 18% 58%,
                rgba(190,202,211,0.78) 0%,
                rgba(165,180,190,0.55) 24%,
                transparent 55%
            ),

            radial-gradient(
                ellipse at 40% 35%,
                rgba(205,215,222,0.82) 0%,
                rgba(170,184,193,0.58) 25%,
                transparent 56%
            ),

            radial-gradient(
                ellipse at 62% 45%,
                rgba(180,194,203,0.72) 0%,
                rgba(135,151,162,0.48) 30%,
                transparent 60%
            ),

            radial-gradient(
                ellipse at 82% 60%,
                rgba(155,170,181,0.68) 0%,
                rgba(100,116,128,0.42) 32%,
                transparent 63%
            ),

            linear-gradient(
                180deg,
                rgba(190,202,211,0.72) 0%,
                rgba(130,145,157,0.58) 55%,
                rgba(65,80,92,0.42) 100%
            );

        box-shadow:
            0 25px 50px
            rgba(
                0,
                0,
                0,
                0.32
            );

        filter:
            blur(8px);
    }}

    .cloud::before {{
        background:

            radial-gradient(
                ellipse at 22% 55%,
                rgba(220,230,236,0.52) 0%,
                transparent 40%
            ),

            radial-gradient(
                ellipse at 44% 30%,
                rgba(220,230,236,0.58) 0%,
                transparent 43%
            ),

            radial-gradient(
                ellipse at 68% 42%,
                rgba(200,213,221,0.42) 0%,
                transparent 42%
            );

        filter:
            blur(20px);
    }}

    .cloud::after {{
        background:

            radial-gradient(
                ellipse,

                rgba(
                    20,
                    30,
                    38,
                    0.28
                ) 0%,

                rgba(
                    50,
                    65,
                    76,
                    0.16
                ) 40%,

                transparent 74%
            );

        filter:
            blur(20px);
    }}

    /* ----------------------------------------------
       DARK RAIN
       ---------------------------------------------- */

    .rain-drop {{
        background:
            linear-gradient(
                180deg,
                rgba(150,190,220,0.0),
                rgba(145,195,230,0.35),
                rgba(175,215,240,0.72),
                rgba(190,225,245,0.12)
            );

        box-shadow:
            0 0 5px
            rgba(
                120,
                180,
                220,
                0.20
            );
    }}

    .rain-ground {{
        background:
            radial-gradient(
                ellipse at center bottom,
                rgba(120,170,205,0.18),
                transparent 68%
            );
    }}
}}


/* ==================================================
   MOBILE
   ================================================== */

@media (max-width: 768px) {{

    .cloud-field {{
        height:
            340px;
    }}

    .cloud {{
        width:
            300px;

        height:
            90px;
    }}

    .cloud-one {{
        top:
            65px;
    }}

    .cloud-two {{
        top:
            125px;
    }}

    .cloud-three {{
        top:
            70px;
    }}

    .cloud-four {{
        top:
            190px;
    }}

    .cloud-five {{
        top:
            260px;
    }}

    .thermal-sun-core {{
        top:
            82px;

        right:
            58px;

        width:
            48px;

        height:
            48px;
    }}

    .environment-indicator {{
        top:
            58px;

        right:
            14px;
    }}

    .rain-drop {{
        height:
            48px;
    }}

    .rain-drop.near {{
        height:
            68px;
    }}
}}

</style>


<!-- ==================================================
     SOLAR ENVIRONMENT
     ================================================== -->

<div class="solar-halo"></div>

<div class="solar-light-field"></div>

<div class="solar-rays"></div>

<div class="solar-content-wash"></div>

<div class="thermal-sun-core"></div>


<!-- ==================================================
     CLOUD ENVIRONMENT
     ================================================== -->

<div class="cloud-field">
    <div class="cloud cloud-one"></div>
    <div class="cloud cloud-two"></div>
    <div class="cloud cloud-three"></div>
    <div class="cloud cloud-four"></div>
    <div class="cloud cloud-five"></div>
</div>


<!-- ==================================================
     ATMOSPHERIC HAZE
     ================================================== -->

<div class="atmospheric-haze"></div>


<!-- ==================================================
     WEATHER DARKNESS
     ================================================== -->

<div class="weather-darkness"></div>


<!-- ==================================================
     STORM LIGHTNING
     ================================================== -->

{storm_effect_html}


<!-- ==================================================
     RAIN PARTICLES
     ================================================== -->

<div class="rain-field">

    <div
        class="rain-drop far"
        style="
            left: 3%;
            --rain-duration: 1.55s;
            --rain-delay: -1.10s;
            --rain-opacity: 0.32;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 8%;
            --rain-duration: 0.92s;
            --rain-delay: -0.42s;
            --rain-opacity: 0.48;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 13%;
            --rain-duration: 0.68s;
            --rain-delay: -0.28s;
            --rain-opacity: 0.70;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 18%;
            --rain-duration: 1.08s;
            --rain-delay: -0.73s;
            --rain-opacity: 0.42;
        "
    ></div>

    <div
        class="rain-drop far"
        style="
            left: 23%;
            --rain-duration: 1.72s;
            --rain-delay: -1.43s;
            --rain-opacity: 0.26;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 28%;
            --rain-duration: 0.74s;
            --rain-delay: -0.52s;
            --rain-opacity: 0.76;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 34%;
            --rain-duration: 1.01s;
            --rain-delay: -0.21s;
            --rain-opacity: 0.50;
        "
    ></div>

    <div
        class="rain-drop far"
        style="
            left: 39%;
            --rain-duration: 1.62s;
            --rain-delay: -1.21s;
            --rain-opacity: 0.28;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 44%;
            --rain-duration: 0.87s;
            --rain-delay: -0.61s;
            --rain-opacity: 0.55;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 49%;
            --rain-duration: 0.64s;
            --rain-delay: -0.17s;
            --rain-opacity: 0.74;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 55%;
            --rain-duration: 1.14s;
            --rain-delay: -0.88s;
            --rain-opacity: 0.45;
        "
    ></div>

    <div
        class="rain-drop far"
        style="
            left: 60%;
            --rain-duration: 1.82s;
            --rain-delay: -1.54s;
            --rain-opacity: 0.24;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 65%;
            --rain-duration: 0.71s;
            --rain-delay: -0.39s;
            --rain-opacity: 0.72;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 70%;
            --rain-duration: 0.96s;
            --rain-delay: -0.67s;
            --rain-opacity: 0.49;
        "
    ></div>

    <div
        class="rain-drop far"
        style="
            left: 76%;
            --rain-duration: 1.68s;
            --rain-delay: -1.27s;
            --rain-opacity: 0.27;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 81%;
            --rain-duration: 0.69s;
            --rain-delay: -0.44s;
            --rain-opacity: 0.78;
        "
    ></div>

    <div
        class="rain-drop"
        style="
            left: 86%;
            --rain-duration: 1.09s;
            --rain-delay: -0.31s;
            --rain-opacity: 0.43;
        "
    ></div>

    <div
        class="rain-drop far"
        style="
            left: 91%;
            --rain-duration: 1.74s;
            --rain-delay: -1.36s;
            --rain-opacity: 0.25;
        "
    ></div>

    <div
        class="rain-drop near"
        style="
            left: 96%;
            --rain-duration: 0.76s;
            --rain-delay: -0.57s;
            --rain-opacity: 0.69;
        "
    ></div>

</div>


<!-- ==================================================
     RAIN GROUND HAZE
     ================================================== -->

<div class="rain-ground"></div>


<!-- ==================================================
     ENVIRONMENT INDICATOR
     ================================================== -->

<div class="environment-indicator">
    {icon}
    {environment_state.label}
</div>
"""

    # ==================================================
    # STREAMLIT HTML RENDERER
    # ==================================================

    st.html(
        environment_html
    )