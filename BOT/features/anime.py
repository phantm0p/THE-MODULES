import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from io import BytesIO

ANILIST_API_URL = "https://graphql.anilist.co"

def get_anime_details(anime_title):
    query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description(asHtml: false)
            episodes
            status
            coverImage {
                large
            }
            averageScore
            genres
            format
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            duration
            studios {
                nodes {
                    name
                }
            }
        }
    }
    '''
    variables = {
        'search': anime_title
    }

    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        return response.json()['data']['Media']
    else:
        raise Exception(f"Query failed to run with a {response.status_code}.")

def create_anime_image(anime_details):
    # Download the cover image
    response = requests.get(anime_details['coverImage']['large'])
    cover_img = Image.open(BytesIO(response.content)).convert('RGBA')

    # Create a blurred background from the cover image
    blurred_bg = cover_img.resize((1280, 720)).filter(ImageFilter.GaussianBlur(15)).convert('RGBA')
    
    # Create a semi-transparent overlay
    overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 150))
    combined_img = Image.alpha_composite(blurred_bg, overlay)

    # Resize cover image
    cover_img = cover_img.resize((320, 480))

    # Create a glow effect around the cover image
    border_size = 10
    glow_img = Image.new('RGBA', (cover_img.width + 2 * border_size, cover_img.height + 2 * border_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(glow_img)
    draw.rectangle([0, 0, glow_img.width, glow_img.height], fill=(255, 255, 255, 255))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(10))

    # Combine the glow with the cover image
    combined_glow_img = Image.new('RGBA', glow_img.size, (0, 0, 0, 0))
    combined_glow_img.paste(glow_img, (0, 0), glow_img)
    combined_glow_img.paste(cover_img, (border_size, border_size), cover_img)

    # Calculate the position to place the cover image with glow in the middle of the background
    bg_width, bg_height = combined_img.size
    img_width, img_height = combined_glow_img.size
    x_position = (bg_width - img_width) // 2
    y_position = (bg_height - img_height) // 2

    # Paste the cover image with glow onto the background
    combined_img.paste(combined_glow_img, (x_position, y_position), combined_glow_img)

    return combined_img.convert('RGB')

if __name__ == "__main__":
    anime_title = input("Enter the title of the anime: ")
    try:
        anime_details = get_anime_details(anime_title)
        image = create_anime_image(anime_details)
        image.show()  # Display the image
        image.save("anime_details.jpg")  # Save the image
        print("Image created successfully.")
    except Exception as e:
        print(e)
