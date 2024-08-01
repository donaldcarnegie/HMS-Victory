import requests
import base64
import html
import uuid
from PIL import Image, ImageChops
from html2image import Html2Image

hti = Html2Image(output_path='.')

def trim(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def read_html_template(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading HTML template {file_path}: {e}")
        return ""

async def create_daily_summary_image(summary_data, title):
    total_members = summary_data['total_members']
    members_joined = summary_data['members_joined']
    members_left = summary_data['members_left']
    members_banned = summary_data['members_banned']
    total_messages = summary_data['total_messages']
    reactions_added = summary_data['reactions_added']
    reactions_removed = summary_data['reactions_removed']
    deleted_messages = summary_data['deleted_messages']
    boosters_gained = summary_data['boosters_gained']
    boosters_lost = summary_data['boosters_lost']
    top_channels = summary_data['top_channels']
    active_members = summary_data['active_members']
    reacting_members = summary_data['reacting_members']

    top_channels_str = '\n'.join([f'<li>{channel_name}: {count} messages</li>' for channel_name, count in top_channels])
    active_members_str = '\n'.join([f'<li>{member_name}: {count} messages</li>' for member_name, count in active_members])
    reacting_members_str = '\n'.join([f'<li>{member_name}: {count} reactions</li>' for member_name, count in reacting_members])

    html_content = read_html_template('templates/daily_summary_grid.html').format(
        title=title,
        total_members=total_members,
        members_joined=members_joined,
        members_left=f"{members_left} ({members_banned} banned)",
        total_messages=total_messages,
        reactions_added=reactions_added,
        reactions_removed=reactions_removed,
        deleted_messages=deleted_messages,
        boosters=f"{boosters_gained} / {boosters_lost}",
        top_channels=top_channels_str,
        active_members=active_members_str,
        reacting_members=reacting_members_str
    )

    output_path = f"{uuid.uuid4()}.png"
    hti.screenshot(html_str=html_content, save_as=output_path, size=(800, 1000))  # Consistent size
    image = Image.open(output_path)
    image = trim(image)
    image.save(output_path)
    return output_path
