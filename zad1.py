from OpenGL.GL import *
import glfw
import glm

from helpers.shaders import ShaderProgram

speed_y = 0.0
speed_x = 0.0
shader = None

def key_callback(window, key, scancode, action, mods):
	global speed_y, speed_x
	if action == glfw.PRESS:
		if key == glfw.KEY_LEFT:
			speed_y = -3.14
		if key == glfw.KEY_RIGHT:
			speed_y = 3.14
		if key == glfw.KEY_UP:
			speed_x = -3.14
		if key == glfw.KEY_DOWN:
			speed_x = 3.14
	if action == glfw.RELEASE:
		if key == glfw.KEY_LEFT or key == glfw.KEY_RIGHT:
			speed_y = 0.0
		if key == glfw.KEY_UP or key == glfw.KEY_DOWN:
			speed_x = 0.0

def init_opengl_program(window):
	global shader

	glClearColor(0, 0, 0, 1)
	shader = ShaderProgram("zad1/v_shader.glsl", "", "zad1/f_shader.glsl")
	glfw.set_key_callback(window, key_callback)


def draw_scene(window, angle_x, angle_y):
	global shader
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	V = glm.lookAt(
		glm.vec3(0.0, 0.0, -5.0),
		glm.vec3(0.0, 0.0, 0.0),
		glm.vec3(0.0, 1.0, 0.0)
	)
	P = glm.perspective(glm.radians(50.0), 1.0, 1.0, 50.0)

	shader.use()
	glUniformMatrix4fv(shader.u("P"), 1, GL_FALSE, P.to_list())
	glUniformMatrix4fv(shader.u("V"), 1, GL_FALSE, V.to_list())

	M = glm.rotate(angle_y, glm.vec3(0, 1, 0)) * glm.rotate(angle_x, glm.vec3(1, 0, 0))
	glUniformMatrix4fv(shader.u("M"), 1, GL_FALSE, M.to_list())


	glfw.swap_buffers(window)

def free_opengl_program(window):
	# Możesz dodać odpowiednie czyszczenie zasobów tutaj, jeśli jest to konieczne
	pass

def main():
	glfw.init()
	window = glfw.create_window(500, 500, "Programowanie multimedialne", None, None)
	glfw.make_context_current(window)
	glfw.swap_interval(1)

	init_opengl_program(window)

	glfw.set_time(0)

	angle_x = 0.0
	angle_y = 0.0

	while not glfw.window_should_close(window):
		time = glfw.get_time()
		glfw.set_time(0.0)

		angle_x += speed_x * time
		angle_y += speed_y * time

		draw_scene(window, angle_x, angle_y)
		glfw.poll_events()


	free_opengl_program(window)
	glfw.terminate()


if __name__ == "__main__":
	main()
