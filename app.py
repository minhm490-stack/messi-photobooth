import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(page_title="Messi Photobooth", layout="centered")

st.title("💖 Pé Naau Photobooth - Chụp Trực Tiếp")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo dải Photostrip siêu dễ thương nhé!")

current_dir = os.path.dirname(os.path.abspath(__file__))
side_images = []
for i in range(1, 5):
    p = os.path.join(current_dir, f"{i}.jpg")
    if os.path.exists(p):
        side_images.append(Image.open(p).convert("RGB"))

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp ảnh")
    cam1 = st.camera_input("Chụp ảnh 1")
    cam2 = st.camera_input("Chụp ảnh 2")

with col2:
    st.subheader("📸 Khung chụp tiếp")
    cam3 = st.camera_input("Chụp ảnh 3")
    cam4 = st.camera_input("Chụp ảnh 4")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list) and len(side_images) == 4:
    if st.button("✨ Tạo Dải Photostrip Ngay", type="primary"):
        webcam_images = [Image.open(f).convert("RGB") for f in captured_list]

        strip_w = 640
        card_w, card_h = 580, 260
        margin_x = (strip_w - card_w) // 2
        margin_y = 20
        header_h = 110
        footer_h = 160

        strip_h = header_h + (card_h * 4) + (margin_y * 5) + footer_h

        strip = Image.new("RGBA", (strip_w, strip_h), (20, 28, 45, 255))
        draw = ImageDraw.Draw(strip)

        stripe_w = 20
        sky_blue = (117, 170, 219, 255)
        gold_color = (212, 175, 55, 255)

        draw.rectangle([(0, 0), (stripe_w, strip_h)], fill=sky_blue)
        draw.rectangle([(strip_w - stripe_w, 0), (strip_w, strip_h)], fill=sky_blue)

        try:
            font_title = ImageFont.truetype("arialbd.ttf", 30)
            font_sub = ImageFont.truetype("arial.ttf", 16)
            font_wish = ImageFont.truetype("arialbd.ttf", 15)
        except IOError:
            font_title = font_sub = font_wish = ImageFont.load_default()

        draw.text((strip_w // 2, 40), "LEGENDARY MESSI", fill=gold_color, font=font_title, anchor="mm")
        draw.text((strip_w // 2, 75), "⭐ ⭐ ⭐ WORLD CHAMPION ⭐ ⭐ ⭐", fill=(255, 215, 0), font=font_sub, anchor="mm")

        sub_w, sub_h = 260, 210
        y_offset = header_h + margin_y

        for idx in range(4):
            card_box = [margin_x, y_offset, margin_x + card_w, y_offset + card_h]
            draw.rounded_rectangle(card_box, radius=20, fill=(30, 40, 60, 255), outline=gold_color, width=3)

            pos_y = y_offset + (card_h - sub_h) // 2

            fitted_user = ImageOps.fit(webcam_images[idx], (sub_w, sub_h), Image.Resampling.LANCZOS)
            mask_w = Image.new("L", (sub_w, sub_h), 0)
            ImageDraw.Draw(mask_w).rounded_rectangle([(0, 0), (sub_w, sub_h)], radius=12, fill=255)
            fitted_user.putalpha(mask_w)

            pos_left_x = margin_x + 20
            draw.rounded_rectangle([pos_left_x - 2, pos_y - 2, pos_left_x + sub_w + 2, pos_y + sub_h + 2], radius=14,
                                   fill=gold_color)
            strip.paste(fitted_user, (pos_left_x, pos_y), mask=fitted_user)

            fitted_side = ImageOps.fit(side_images[idx], (sub_w, sub_h), Image.Resampling.LANCZOS)
            mask_s = Image.new("L", (sub_w, sub_h), 0)
            ImageDraw.Draw(mask_s).rounded_rectangle([(0, 0), (sub_w, sub_h)], radius=12, fill=255)
            fitted_side.putalpha(mask_s)

            pos_right_x = margin_x + card_w - sub_w - 20
            draw.rounded_rectangle([pos_right_x - 2, pos_y - 2, pos_right_x + sub_w + 2, pos_y + sub_h + 2], radius=14,
                                   fill=gold_color)
            strip.paste(fitted_side, (pos_right_x, pos_y), mask=fitted_side)

            y_offset += card_h + margin_y

        sun_x = strip_w // 2
        sun_y = y_offset + 25
        draw.ellipse([(sun_x - 14, sun_y - 14), (sun_x + 14, sun_y + 14)], fill=(246, 180, 14, 255), outline=gold_color,
                     width=2)

        draw.text((sun_x, y_offset + 60), "PE NAAU NUMBER ONE", fill=gold_color, font=font_wish,
                  anchor="mm")
        draw.text((sun_x, y_offset + 85), "🌟 ⭐ 🌟", fill=gold_color, font=font_wish,
                  anchor="mm")

        final_output = Image.new("RGB", strip.size, (255, 255, 255))
        final_output.paste(strip, mask=strip.split()[3])

        st.success("🎉 Đã tạo thành công dải Photostrip!")
        st.image(final_output, caption="Dải Photostrip của bạn", use_container_width=True)

        output_path = os.path.join(current_dir, "output_photostrip.jpg")
        final_output.save(output_path, quality=95)
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Tải ảnh về máy",
                data=file,
                file_name="messi_photostrip.jpg",
                mime="image/jpeg"
            )
else:
    st.info("💡 Hãy dùng webcam chụp đủ **4 bức ảnh** ở trên để nút tạo ảnh xuất hiện nhé!")
