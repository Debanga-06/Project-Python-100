import streamlit as st
from PIL import Image

from src.preprocess import (
    get_image_details,
    grayscale_image,
    edge_detection,
    blur_image,
    calculate_brightness,
    calculate_contrast,
    average_rgb
)

from src.visualization import (
    plot_rgb_histogram,
    plot_brightness,
    plot_rgb_bar
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Image Recognition Classifier",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

def load_css():

    try:

        with open(
            "styles/style.css",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except:
        pass


load_css()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🧠 AI Dashboard")

    st.markdown("---")

    st.subheader("Project")

    st.write("Image Recognition Classifier")

    st.markdown("---")

    st.subheader("Technology")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• OpenCV")
    st.write("• Pillow")
    st.write("• NumPy")
    st.write("• Matplotlib")

    st.markdown("---")

    st.success("Demo Version 1.0")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🖼️ Image Recognition Classifier")

st.write(
    """
Upload an image and analyze it using Computer Vision.

This project demonstrates image preprocessing,
visualization and AI-ready analysis.
"""
)

st.divider()

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)

# ---------------------------------------------------
# IMAGE ANALYSIS
# ---------------------------------------------------

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    details = get_image_details(
        image,
        uploaded_file
    )

    gray = grayscale_image(image)

    edges = edge_detection(image)

    blur = blur_image(image)

    brightness = calculate_brightness(image)

    contrast = calculate_contrast(image)

    rgb = average_rgb(image)

    histogram = plot_rgb_histogram(image)

    brightness_chart = plot_brightness(
        brightness
    )

    rgb_chart = plot_rgb_bar(
        rgb
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Image",
            "Analysis",
            "Charts"
        ]
    )
    # -----------------------------
    # TAB 1 : IMAGES
    # -----------------------------
    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📷 Original Image")
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("🖤 Grayscale Image")
            st.image(gray, use_container_width=True)

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✨ Edge Detection")
            st.image(edges, use_container_width=True)

        with col4:
            st.subheader("🌫️ Blurred Image")
            st.image(blur, use_container_width=True)

    # -----------------------------
    # TAB 2 : ANALYSIS
    # -----------------------------
    with tab2:

        st.subheader("📊 Image Information")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Width", f"{details['width']} px")
            st.metric("Height", f"{details['height']} px")
            st.metric("Mode", details["mode"])

        with c2:
            st.metric("Format", details["format"])
            st.metric("File Size", f"{details['size_kb']} KB")
            st.metric("Contrast", contrast)

        st.divider()

        st.subheader("🎨 Average RGB Values")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("🔴 Red", rgb["R"])

        with r2:
            st.metric("🟢 Green", rgb["G"])

        with r3:
            st.metric("🔵 Blue", rgb["B"])

        st.divider()

        st.subheader("🌞 Brightness")

        st.metric(
            "Average Brightness",
            brightness
        )

        st.pyplot(
            brightness_chart,
            use_container_width=True
        )

    # -----------------------------
    # TAB 3 : CHARTS
    # -----------------------------
    with tab3:

        st.subheader("📈 RGB Histogram")

        st.pyplot(
            histogram,
            use_container_width=True
        )

        st.divider()

        st.subheader("📊 RGB Distribution")

        st.pyplot(
            rgb_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("🤖 AI Prediction")

    st.success("Prediction Completed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Detected Object",
            "Temple"
        )

    with col2:
        st.metric(
            "Confidence",
            "98.71%"
        )

    with col3:
        st.metric(
            "Model",
            "Demo v1.0"
        )

    st.info(
        """
⚠️ This is a demonstration prediction.

The current version focuses on image analysis using OpenCV.

A real deep learning model will be integrated in Version 2.0.
"""
    )

else:

    st.info("👆 Upload an image to begin analysis.")

st.divider()

footer1, footer2, footer3 = st.columns(3)

with footer1:
    st.metric("Framework", "Streamlit")

with footer2:
    st.metric("Computer Vision", "OpenCV")

with footer3:
    st.metric("Status", "Ready")

st.caption(
    "© 2026 | Image Recognition Classifier | Project 10 | Python • OpenCV • Streamlit"
)