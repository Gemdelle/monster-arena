# import pygame
# from PIL import Image

# pygame.init()

# # Load the animated GIF using Pillow
# gif = Image.open("assets/giphy.gif")

# # Get the number of frames in the GIF
# num_frames = gif.n_frames

# # Create a Pygame window
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Monster Arena")

# # Set the frame rate (adjust as needed)
# frame_rate = 25
# clock = pygame.time.Clock()

# running = True
# frame_index = 0

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     try:
#         gif.seek(frame_index)  # Go to the specified frame
#         frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
#     except EOFError:
#         frame_index = 0
#         gif.seek(frame_index)
#         frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)

#     screen.blit(frame, (0, 0))
#     pygame.display.flip()

#     clock.tick(frame_rate)
#     frame_index += 1

#     if frame_index >= num_frames:
#         frame_index = 0

# pygame.quit()