#include <iostream>
#include <math.h>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <stb_image.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "Object.h"

using namespace std;

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void keyCallback(GLFWwindow* window, int key, int scancode, int action, int mods);
unsigned int createShader(const char* filename, const char* type);
unsigned int createProgram(unsigned int vertexShader, unsigned int geometryShader, unsigned int fragmentShader);
unsigned int ModelVAO(Object* model);
void LoadTexture(unsigned int& texture, const char* tFileName);
glm::mat4 getPerspective();
glm::mat4 getView();

Object* deerModel = new Object("obj/Deer.obj");

int windowWidth = 800, windowHeight = 600;


float angle = 0;
float speed = 0;
float speed3 = 0.1;
float speed2 = 0.05;
float speed4 = 0.15;
bool re = false;

bool noGS = false;
float mode = 0;
bool isRotate = false;
bool stop = false;

bool iswind=true;
//wind_strength means how fast the fur affect by wind
float wind_strength = 0.019;
//wind_threshold means how long can the fur extend
float wind_threshold = 0.03;

glm::vec3 winddir = glm::vec3(1.0,0.0,0.0);


/*
##################CAUTION!!##################
This is just an example code just for the basicest demo purpose.
Unlike previous HW2,HW3 that only required to fill in the TODO part,
in this assignment you are expected to design your own work.
You can modify or even delete most of the template during your design process,
but if you submit a code "very very" simliar to the example  code's geometry effect,
your score will be 0
##################CAUTION!!##################
*/




int main()
{
	// Initialization
	glfwInit();
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
	glfwWindowHint(GLFE_OPENGL_FORWARD_COMPACT, GL_TRUE);
#endif

	GLFWwindow* window = glfwCreateWindow(windowWidth, windowHeight, "HW4", NULL, NULL);
	if (window == NULL)
	{
		std::cout << "Failed to create GLFW window" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	glfwSetKeyCallback(window, keyCallback);
	glfwSwapInterval(1);

	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}

	// Shaders
	unsigned int vertexShader, fragmentShader, geometryShader, shaderProgram;
	vector<unsigned int> programs;
	vertexShader = createShader("shaders/deer.vert", "vert");
	fragmentShader = createShader("shaders/deer.frag", "frag");
	shaderProgram = createProgram(vertexShader, 0, fragmentShader);
	programs.push_back(shaderProgram);
	
	vertexShader = createShader("shaders/normal.vert", "vert");
	geometryShader = createShader("shaders/normal.geom", "geom");
	fragmentShader = createShader("shaders/normal.frag", "frag");
	shaderProgram = createProgram(vertexShader, geometryShader, fragmentShader);
	programs.push_back(shaderProgram);

	// Texture
	unsigned int deerTexture;
	LoadTexture(deerTexture, "obj/Deer_diffuse.jpg");

	// VAO, VBO
	unsigned int deerVAO;
	deerVAO = ModelVAO(deerModel);

	// Display loop
	glfwGetFramebufferSize(window, &windowWidth, &windowHeight);
	glViewport(0, 0, windowWidth, windowHeight);
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LEQUAL);
	double dt;
	double lastTime = glfwGetTime();
	double currentTime;
	unsigned int mLoc, vLoc, pLoc, normalMLoc,windshiftLoc;


	glm::vec3 windshift = glm::vec3(0.0);
	float windshift_amount = 0.0;

	int float_animate = 1.0;// 1 for blowing and -1 for returning

	while (!glfwWindowShouldClose(window))
	{
		glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		glm::mat4 perspective = getPerspective();
		glm::mat4 view = getView();
		glm::mat4 model = glm::mat4(1.0f);

		model = glm::translate(model, glm::vec3(0.0, -1.5, 0.7));
		model = glm::rotate(model, angle, glm::vec3(0, 1, 0));
		model = glm::rotate(model, glm::radians(-120.0f), glm::vec3(0, 1, 0));
		model = glm::rotate(model, glm::radians(-90.0f), glm::vec3(1, 0, 0));
		model = glm::scale(model, glm::vec3(0.05, 0.05, 0.05));

		glm::mat4 normalM = glm::transpose(glm::inverse(model));

		size_t n = programs.size();

		//for (unsigned int program : programs)  
		for(int i=0;i<n;++i)
		{
			if (i == 0 && !noGS) continue;
			if (i == 1 && noGS) continue;
			// i==1 means geometry progream
			glUseProgram(programs[i]);
			mLoc = glGetUniformLocation(programs[i], "M");
			vLoc = glGetUniformLocation(programs[i], "V");
			pLoc = glGetUniformLocation(programs[i], "P");
			normalMLoc = glGetUniformLocation(programs[i], "normalM");
			windshiftLoc = glGetUniformLocation(programs[i], "windshift");

			glUniformMatrix4fv(mLoc, 1, GL_FALSE, glm::value_ptr(model));
			glUniformMatrix4fv(vLoc, 1, GL_FALSE, glm::value_ptr(view));
			glUniformMatrix4fv(pLoc, 1, GL_FALSE, glm::value_ptr(perspective));
			glUniformMatrix4fv(normalMLoc, 1, GL_FALSE, glm::value_ptr(normalM));
			glUniform3fv(windshiftLoc, 1, glm::value_ptr(windshift));
			glUniform1f(glGetUniformLocation(programs[i], "mode"), mode);
			glUniform1f(glGetUniformLocation(programs[i], "speed"), speed);
			glUniform1f(glGetUniformLocation(programs[i], "speed3"), speed3);
			glUniform1f(glGetUniformLocation(programs[i], "speed2"), speed2);
			glUniform1f(glGetUniformLocation(programs[i], "speed4"), speed4);

			glActiveTexture(GL_TEXTURE0);
			glBindTexture(GL_TEXTURE_2D, deerTexture);

			glBindVertexArray(deerVAO);
			glDrawArrays(GL_TRIANGLES, 0, deerModel->positions.size());
			glBindTexture(GL_TEXTURE_2D, 0);
			glBindVertexArray(0);
		}

		// Status update
		currentTime = glfwGetTime();
		dt = currentTime - lastTime;
		lastTime = currentTime;
		if (isRotate) angle += glm::radians(90.0f) * dt;
		if (stop && (mode == 1 || mode == 2 || mode == 4)) {
			if (speed > 0.2 || speed < -0.2) {
				re = !re;
			}
			if (re) {
				speed = speed + dt * 0.5;
			}
			else {
				speed = speed - dt * 0.5;
			}
			speed2 += dt;
			if (speed2 > 5) {
				speed2 = 0;
			}
			speed4 += dt;
			if (speed4 > 5) {
				speed4 = 5;
			}
		}
		if (stop && mode == 3) {
			if (speed > 0.2 || speed < -0.2) {
				re = !re;
			}
			if (re) {
				speed = speed + dt * 0.8;
			}
			else {
				speed = speed - dt * 0.8;
			}
			if (re) {
				speed3 = speed + 0.1;
				if (speed3 > 0.2) {
					speed3 = 0.4 - speed3;
				}
			}
			else
			{
				speed3 = speed - 0.1;
				if (speed3 < -0.2) {
					speed3 = -0.4 - speed3;
				}
			}
		}
		if (stop && mode == 5) {
			if (speed > 0.2 || speed < -0.2) {
				re = !re;
			}
			if (re) {
				speed = speed + dt*1.2;
			}
			else {
				speed = speed - dt*1.2;
			}
			if (re) {
				speed2 = speed + 0.05;
				if (speed2 > 0.2) {
					speed2 = 0.4 - speed2;
				}
			}
			else
			{
				speed2 = speed - 0.05;
				if (speed2 < -0.2) {
					speed2 = -0.4 - speed2;
				}
			}
			if (re) {
				speed3 = speed + 0.1;
				if (speed3 > 0.2) {
					speed3 = 0.4 - speed3;
				}
			}
			else
			{
				speed3 = speed - 0.1;
				if (speed3 < -0.2) {
					speed3 = -0.4 - speed3;
				}
			}
			if (re) {
				speed4 = speed + 0.15;
				if (speed4 > 0.2) {
					speed4 = 0.4 - speed4;
				}
			}
			else
			{
				speed4 = speed - 0.15;
				if (speed4 < -0.2) {
					speed4 = -0.4 - speed4;
				}
			}
		}
		//A very very simple wind simulation just for demo,
		if (iswind) {
			if (windshift_amount < 0) float_animate = 1.0;
			if (windshift_amount > wind_threshold) float_animate = -1.0;

			windshift_amount += float_animate * dt * wind_strength;
			windshift = winddir * windshift_amount;
		}
		else windshift = glm::vec3(0.0);

		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	glfwTerminate();
	return 0;
}

// Add key callback
void keyCallback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, true);

	if (key == GLFW_KEY_R && action == GLFW_PRESS)
	{
		isRotate=!isRotate;
		cout << "KEY R PRESSED\n";
	}
	if (key == GLFW_KEY_D && action == GLFW_PRESS)
	{
		noGS = 1;
		mode = 0;
		cout << "KEY D PRESSED\n";
	}
	if (key == GLFW_KEY_G && action == GLFW_PRESS)
	{
		noGS = 0;
		mode = 1;
		stop = 1;
		speed4 = 0;
		cout << "KEY G PRESSED\n";
	}
	if (key == GLFW_KEY_S && action == GLFW_PRESS)
	{
		stop = !stop;
		cout << "KEY S PRESSED\n";
	}
	if (key == GLFW_KEY_W && action == GLFW_PRESS)
	{
		noGS = 0;
		mode = 2;
		stop = 1;
		speed = 0;
		speed3 = 0.1;
		cout << "KEY W PRESSED\n";
	}
	if (key == GLFW_KEY_U && action == GLFW_PRESS)
	{
		noGS = 0;
		mode = 3;
		stop = 1;
		speed = 0;
		speed3 = 0.1;
		cout << "KEY U PRESSED\n";
	}
	if (key == GLFW_KEY_N && action == GLFW_PRESS)
	{
		noGS = 0;
		mode = 4;
		stop = 1;
		speed = 0;
		speed3 = 0.1;
		speed2 = 0;
		cout << "KEY N PRESSED\n";
	}
	if (key == GLFW_KEY_H && action == GLFW_PRESS)
	{
		noGS = 0;
		mode = 5;
		stop = 1;
		speed = 0;
		speed3 = 0.1;
		speed2 = 0.05;
		speed4 = 0.15;
		cout << "KEY H PRESSED\n";
	}
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
	glViewport(0, 0, width, height);
	windowWidth = width;
	windowHeight = height;
}

unsigned int createShader(const char* filename, const char* type)
{
	unsigned int shader;
	if (strcmp(type, "vert") == 0)
		shader = glCreateShader(GL_VERTEX_SHADER);
	else if (strcmp(type, "frag") == 0)
		shader = glCreateShader(GL_FRAGMENT_SHADER);
	else if (strcmp(type, "geom") == 0)
		shader = glCreateShader(GL_GEOMETRY_SHADER);
	else
	{
		cout << "Unknown Shader Type.\n";
		return 0;
	}

	FILE* fp = fopen(filename, "rb");
	fseek(fp, 0, SEEK_END);
	long fsize = ftell(fp);
	fseek(fp, 0, SEEK_SET);  //same as rewind(fp);

	char* source = (char*)malloc(sizeof(char) * (fsize + 1));
	fread(source, fsize, 1, fp);
	fclose(fp);

	source[fsize] = 0;

	glShaderSource(shader, 1, &source, NULL);
	glCompileShader(shader);

	int success;
	char infoLog[512];
	glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(shader, 512, NULL, infoLog);
		cout << "ERROR::SHADER::" << type << "::COMPLIATION_FAILED\n" << infoLog << endl;
		return -1;
	}

	return shader;
}

unsigned int createProgram(unsigned int vertexShader, unsigned int geometryShader, unsigned int fragmentShader)
{
	unsigned int program = glCreateProgram();

	//Attach our shaders to our program
	glAttachShader(program, vertexShader);
	glAttachShader(program, geometryShader);
	glAttachShader(program, fragmentShader);

	//Link our program
	glLinkProgram(program);

	//Note the different functions here: glGetProgram* instead of glGetShader*.
	int success = 0;
	glGetProgramiv(program, GL_LINK_STATUS, &success);

	if (!success)
	{
		int maxLength = 0;
		glGetProgramiv(program, GL_INFO_LOG_LENGTH, &maxLength);

		//The maxLength includes the NULL character
		char* infoLog = (char*)malloc(sizeof(char) * (maxLength));
		glGetProgramInfoLog(program, maxLength, &maxLength, infoLog);

		//We don't need the program anymore.
		glDeleteProgram(program);
		//Don't leak shaders either.
		glDeleteShader(vertexShader);
		glDeleteShader(fragmentShader);

		cout << "LINKING ERROR: ";
		puts(infoLog);
		free(infoLog);

		return -1;
	}

	//Always detach shaders after a successful link.
	glDetachShader(program, vertexShader);
	glDetachShader(program, fragmentShader);

	return program;
}

unsigned int ModelVAO(Object* model)
{
	unsigned int VAO, VBO[3];
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);
	glGenBuffers(3, VBO);

	glBindBuffer(GL_ARRAY_BUFFER, VBO[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(GL_FLOAT) * (model->positions.size()), &(model->positions[0]), GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(GL_FLOAT) * 3, 0);
	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	glBindBuffer(GL_ARRAY_BUFFER, VBO[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(GL_FLOAT) * (model->normals.size()), &(model->normals[0]), GL_STATIC_DRAW);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(GL_FLOAT) * 3, 0);
	glEnableVertexAttribArray(1);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	glBindBuffer(GL_ARRAY_BUFFER, VBO[2]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(GL_FLOAT) * (model->texcoords.size()), &(model->texcoords[0]), GL_STATIC_DRAW);
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, sizeof(GL_FLOAT) * 2, 0);
	glEnableVertexAttribArray(2);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	glBindVertexArray(0);

	return VAO;
}

void LoadTexture(unsigned int& texture, const char* tFileName) {
	glEnable(GL_TEXTURE_2D);
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	int width, height, nrChannels;
	stbi_set_flip_vertically_on_load(true);
	unsigned char* data = stbi_load(tFileName, &width, &height, &nrChannels, 0);

	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	glBindTexture(GL_TEXTURE_2D, 0);
	stbi_image_free(data);
}

glm::mat4 getPerspective()
{
	return glm::perspective(
		glm::radians(45.0f),
		(float)windowWidth / (float)windowHeight, 
		1.0f, 100.0f);
}

glm::mat4 getView()
{
	return glm::lookAt(
		glm::vec3(0, 3, 5),
		glm::vec3(0, 0, 0),
		glm::vec3(0, 1, 0));
}