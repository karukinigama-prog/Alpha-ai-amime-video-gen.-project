from ursina import *
from ursina.shaders import lit_with_shadows_shader
import os
import shutil

# 1. පද්ධතිය සකස් කිරීම (Headless rendering setup)
# දර්ශනයක් නොපෙන්වා සර්වර් එක ඇතුළේ වැඩ කිරීමට offscreen mode භාවිතා කරයි
app = Ursina(window_type='offscreen', size=(1280, 720))

def run_render():
    # 2. මූලික පරිසරය සැකසීම
    Sky()
    # ආලෝකය සැකසීම (Shader Error මඟහැරීමට ප්ලැට්ෆෝම් එකට ගැලපෙන ලෙස)
    sun = DirectionalLight()
    sun.look_at(Vec3(1, -1, 1))
    
    print("Alpha AI Renderer active - Developed by Hasith")
    
    # 3. GPT-4 ජනනය කළ ඇනිමේෂන් කෝඩ් එක ක්‍රියාත්මක කිරීම
    if os.path.exists("animation_logic.py"):
        print("Executing AI generated logic...")
        try:
            with open("animation_logic.py", "r") as f:
                exec(f.read())
        except Exception as e:
            print(f"Error in animation logic: {e}")
            # වැරැද්දක් වුණොත් පෙන්වීමට මූලික වස්තුවක්
            Entity(model='sphere', color=color.cyan, y=1)
    else:
        print("Warning: animation_logic.py not found!")
        Entity(model='cube', color=color.red)

    # 4. වීඩියෝ රාමු (Frames) සුරැකීමට ෆෝල්ඩරය සකස් කිරීම
    frames_dir = 'frames'
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir) # පරණ ඒවා මකා දැමීම
    os.mkdir(frames_dir)
    
    # 5. රෙන්ඩර් කිරීමේ ක්‍රියාවලිය (තත්පර 5ක වීඩියෝවක් - 150 frames)
    print("Starting frame capture...")
    for i in range(150):
        # එන්ජිම එක පියවරක් ඉදිරියට ගෙන යාම
        app.step()
        # ෆ්‍රේම් එක පින්තූරයක් ලෙස සේව් කිරීම
        image_path = os.path.join(frames_dir, f'f_{i:04d}.png')
        base.screenshot(image_path, defaultFilename=False)
        
        if i % 30 == 0:
            print(f"Rendered {i} frames...")

    # 6. FFmpeg මගින් වීඩියෝව නිපදවීම
    print("Encoding video using FFmpeg...")
    # පින්තූර 150 එකතු කර output.mp4 සාදයි
    ffmpeg_cmd = (
        "ffmpeg -y -framerate 30 -i frames/f_%04d.png "
        "-c:v libx264 -pix_fmt yuv420p -crf 23 output.mp4"
    )
    
    return_code = os.system(ffmpeg_cmd)
    
    if return_code == 0:
        print("Alpha AI: Video generation completed successfully! (output.mp4)")
    else:
        print("Alpha AI: Error during video encoding.")

if __name__ == "__main__":
    run_render()
