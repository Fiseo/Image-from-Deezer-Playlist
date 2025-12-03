from PIL import Image, ImageDraw, ImageFont
import requests, re


playlist_id = # Insert the Id of your playlist
download_path = r"" # Insert the path to the folder which you want to contain the pictures



response = None
try:
    response = requests.get("https://api.deezer.com/playlist/" + str(playlist_id)).json()
except Exception  as e:
    print(f"Unable to connect to the playlist : {e}")

if response is not None:
    playlist_title = response["title"]
    playlist_creator = response["creator"]["name"]
    print(f"Connection with the playlist {playlist_title} by {playlist_creator} done")

    tracks_data = response["tracks"]["data"]

    for track in tracks_data:
        title = track["title"]
        title_safe = re.sub(r'[\\/*?:"<>|]', "",title)
        title_snake_case = re.sub(r'[ ]', "_", title_safe)
        title_jpg = f"{title_snake_case}.jpg"
        img_path = f"{download_path}\\{title_jpg}"

        try:
            with open(img_path, "wb") as f:
                image = requests.get(track["album"]["cover_big"])
                f.write(image.content)
        except Exception  as e:
            print(f"Error while collecting the picture for {title} : {e}")

        try:
            img = Image.open(img_path)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            draw = ImageDraw.Draw(img)

            width, height = img.size
            margin_x = int(width * 0.02)
            margin_y = int(height * 0.02)

            x = margin_x
            y = height - margin_y

            font = ImageFont.truetype("./font.ttf", 35)
            draw.text(
                xy=(x, y),
                anchor="lb",
                text=title,
                font=font,
                fill=(255, 255, 255),
                stroke_width=5,
                stroke_fill=(0,0,0),
            )
            img.save(img_path)
        except Exception  as e:
            print(f"Error while modifying the picture for {title} : {e}")

        print(f"The picture for {title} has been done without problem")
