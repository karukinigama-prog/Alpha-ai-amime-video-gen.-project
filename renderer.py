from ursina import *
from ursina.shaders import lit_with_shadows_shader
import os
import importlib

# Offscreen rendering setup
app = Ursina(window_type='offscreen', borderless=False)

def start_render():
    # අලංකාර පසුබිමක් සහ ආලෝකය
    Entity.default_shader = lit_with_shadows_shader
    DirectionalLight(y=2, z=-3, shadows=True)
    Sky(color=color.light_gray)

    # GPT-4 ලියූ කෝඩ් එක load කිරීම
    try:
        import animation_logic
        print("Logic loaded successfully.")
    except Exception as e:
        print(f"Error loading logic: {e}")
        # Default දර්ශනයක් (කෝඩ් එකක් නැතිනම්)
        Entity(model='cube', color=color.orange, y=1)

    # Frame by Frame පින්තූර ගැනීම
    frames_dir = 'frames'
    if not os.path.exists(frames_dir): os.mkdir(frames_dir)
    
    duration = 5 # තත්පර 5ක වීඩියෝවක්
    fps = 30
    
    for i in range(duration * fps):
        # මෙහිදී animation_logic එකේ update functions තිබේ නම් ඒවා ක්‍රියාත්මක වේ
        app.step() 
        base.screenshot(name=f'{frames_dir}/f_{i:04d}.png', defaultFilename=False)

    # FFmpeg මගින් වීඩියෝව සැකසීම
    os.system(f"ffmpeg -y -framerate {fps} -i {frames_dir}/f_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4")

if __name__ == "__main__":
    start_render()
