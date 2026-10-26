import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Chụp Trực Tiếp")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo dải Photostrip sinh nhật siêu dễ thương nhé!")

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
        header_h = 130
        footer_h = 160

        strip_h = header_h + (card_h * 4) + (margin_y * 5) + footer_h

        # Nền màu TRẮNG HỒNG
        bg_pink_white = (255, 240, 245, 255)
        strip = Image.new("RGBA", (strip_w, strip_h), bg_pink_white)
        draw = ImageDraw.Draw(strip)

        stripe_w = 20
        border_pink = (255, 150, 180, 255)
        card_bg_color = (255, 255, 255, 255)
        frame_outline = (255, 105, 180, 255)
        text_pink_color = (219, 62, 115, 255)

        draw.rectangle([(0, 0), (stripe_w, strip_h)], fill=border_pink)
        draw.rectangle([(strip_w - stripe_w, 0), (strip_w, strip_h)], fill=border_pink)

        try:
            font_title = ImageFont.truetype("arialbd.ttf", 28)
            font_sub = ImageFont.truetype("arialbd.ttf", 16)
            font_wish = ImageFont.truetype("arialbd.ttf", 16)
        except IOError:
            font_title = font_sub = font_wish = ImageFont.load_default()

        def draw_flower(draw_obj, cx, cy, petal_color, center_color, size=8):
            for dx, dy in [(-size, 0), (size, 0), (0, -size), (0, size), (-size*0.7, -size*0.7), (size*0.7, size*0.7), (-size*0.7, size*0.7), (size*0.7, -size*0.7)]:
                draw_obj.ellipse([(cx + dx - size/2, cy + dy - size/2), (cx + dx + size/2, cy + dy + size/2)], fill=petal_color)
            draw_obj.ellipse([(cx - size/2, cy - size/2), (cx + size/2, cy + size/2)], fill=center_color)

        # --- PHẦN HEADER ---
        draw.text((strip_w // 2, 45), "🎉 HAPPY BIRTHDAY 🎉", fill=text_pink_color, font=font_title, anchor="mm")
        draw.text((strip_w // 2, 85), "🌸 KHÁNH HOÀ C CUTIE 🌸", fill=(255, 105, 180), font=font_sub, anchor="mm")

        draw_flower(draw, 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)
        draw_flower(draw, strip_w - 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)

        sub_w, sub_h = 260, 210
        y_offset = header_h + margin_y

        for idx in range(4):
            card_box = [margin_x, y_offset, margin_x + card_w, y_offset + card_h]
            draw.rounded_rectangle(card_box, radius=20, fill=card_bg_color, outline=frame_outline, width=3)

            pos_y = y_offset + (card_h - sub_h) // 2

            fitted_user = ImageOps.fit(webcam_images[idx], (sub_w, sub_h), Image.Resampling.LANCZOS)
            mask_w = Image.new("L", (sub_w, sub_h), 0)
            ImageDraw.Draw(mask_w).rounded_rectangle([(0, 0), (sub_w, sub_h)], radius=12, fill=255)
            fitted_user.putalpha(mask_w)

            pos_left_x = margin_x + 20
            draw.rounded_rectangle([pos_left_x - 2, pos_y - 2, pos_left_x + sub_w + 2, pos_y + sub_h + 2], radius=14, fill=frame_outline)
            strip.paste(fitted_user, (pos_left_x, pos_y), mask=fitted_user)

            fitted_side = ImageOps.fit(side_images[idx], (sub_w, sub_h), Image.Resampling.LANCZOS)
            mask_s = Image.new("L", (sub_w, sub_h), 0)
            ImageDraw.Draw(mask_s).rounded_rectangle([(0, 0), (sub_w, sub_h)], radius=12, fill=255)
            fitted_side.putalpha(mask_s)

            pos_right_x = margin_x + card_w - sub_w - 20
            draw.rounded_rectangle([pos_right_x - 2, pos_y - 2, pos_right_x + sub_w + 2, pos_y + sub_h + 2], radius=14, fill=frame_outline)
            strip.paste(fitted_side, (pos_right_x, pos_y), mask=fitted_side)

            y_offset += card_h + margin_y

        # --- PHẦN FOOTER ---
        center_x = strip_w // 2
        flower_y = y_offset + 30
        
        draw_flower(draw, center_x - 80, flower_y, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=12)
        draw_flower(draw, center_x, flower_y - 10, petal_color=(255, 105, 180), center_color=(255, 255, 0), size=14)
        draw_flower(draw, center_x + 80, flower_y, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=12)

        draw.text((center_x, y_offset + 75), "✨ CHÚC MỪNG SINH NHẬT KHÁNH HOÀ ✨", fill=text_pink_color, font=font_wish, anchor="mm")
        draw.text((center_x, y_offset + 105), "💖 MÃI XINH ĐẸP VÀ HẠNH PHÚC NHÉ! 💖", fill=(233, 30, 99), font=font_wish, anchor="mm")

        final_output = Image.new("RGB", strip.size, (255, 255, 255))
        final_output.paste(strip, mask=strip.split()[3])

        st.success("🎉 Đã tạo thành công dải Photostrip sinh nhật!")
        st.image(final_output, caption="Dải Photostrip của Khánh Hoà", use_container_width=True)

        output_path = os.path.join(current_dir, "output_photostrip.jpg")
        final_output.save(output_path, quality=95)
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Tải ảnh về máy",
                data=file,
                file_name="khanh_hoa_birthday_photostrip.jpg",
                mime="image/jpeg"
            )
else:
    st.info("💡 Hãy dùng webcam chụp đủ **4 bức ảnh** ở trên để nút tạo ảnh xuất hiện nhé!")
