#version 330 core

layout (triangles) in;
layout (triangle_strip, max_vertices = 105) out;
//Input/Output part is important, so be sure to check how everything works

in VS_OUT {
	vec3 normal;
	vec3 fragpos;
	vec2 texCoord;
	vec3 bPos;
} gs_in[];

uniform mat4 M;
uniform mat4 V;
uniform mat4 P;
uniform vec3 windshift;
uniform float mode;
uniform float speed;
uniform float speed3;
uniform float speed2;
uniform float speed4;

out vec3 fragposGS;
out vec3 normalGS;
out vec2 texCoordGS;
out float alphaGS;

vec4 worldPos;
float newspeed;

void main()
{
	if(mode==5){
		alphaGS=0.0;
		for (int i = 0; i < gl_in.length(); ++i) {
			vec3 newPos=gs_in[i].bPos;
			newspeed=(speed+speed3)/2;
			if(newPos.z < 22 && newPos.x > -23){
				if(newPos.x < 0){
					if(newPos.y < 0){
						newPos.x = newPos.x + (newPos.z-22)*speed3*3;
					}else{
						newPos.x = newPos.x + (newPos.z-22)*speed*3;
					}
				}else{
					if(newPos.y > 0){
						newPos.x = newPos.x - (newPos.z-22)*speed3*3;
					}else{
						newPos.x = newPos.x - (newPos.z-22)*speed*3;
					}
				}
				if(speed < 0){
					newPos.z = newPos.z*(1+newspeed*2);
				}else{
					newPos.z = newPos.z*(1-newspeed*2);
				}
			}else{
				if(speed < 0){
					newPos.z = newPos.z+newspeed*40;
				}else{
					newPos.z = newPos.z-newspeed*40;
				}
			}
			worldPos = M * vec4(newPos, 1.0);
			gl_Position = V * worldPos;
			gl_Position = P * gl_Position;
			gl_Position.z+=0.1;
			fragposGS = vec3(worldPos);
			normalGS = normalize(gs_in[i].normal);
			texCoordGS = gs_in[i].texCoord;
			EmitVertex();  
			}
		EndPrimitive();
		alphaGS=1.0;
		for (int i = 0; i < gl_in.length(); ++i) {
			vec3 newPos=gs_in[i].bPos;
			newspeed=(speed2+speed4)/2;
			if(newPos.z < 22 && newPos.x > -23){
				if(newPos.x < 0){
					if(newPos.y < 0){
						newPos.x = newPos.x + (newPos.z-22)*speed4*3;
					}else{
						newPos.x = newPos.x + (newPos.z-22)*speed2*3;
					}
				}else{
					if(newPos.y > 0){
						newPos.x = newPos.x - (newPos.z-22)*speed4*3;
					}else{
						newPos.x = newPos.x - (newPos.z-22)*speed2*3;
					}
				}
				if(newspeed < 0){
					newPos.z = newPos.z*(1+newspeed*2);
				}else{
					newPos.z = newPos.z*(1-newspeed*2);
				}
			}else{
				if(newspeed < 0){
					newPos.z = newPos.z+newspeed*40;
				}else{
					newPos.z = newPos.z-newspeed*40;
				}
			}
			worldPos = M * vec4(newPos, 1.0);
			gl_Position = V * worldPos;
			gl_Position = P * gl_Position;
			fragposGS = vec3(worldPos);
			normalGS = normalize(gs_in[i].normal);
			texCoordGS = gs_in[i].texCoord;
			EmitVertex();  
			}
		EndPrimitive();
	}else if(mode==4){
		for (int j=0;j<35;j++){
			for (int i = 0; i < gl_in.length(); ++i) {
				vec3 newPos=gs_in[i].bPos;
				if( newPos.z < 15){
					if(newPos.x < 0){
						if(newPos.y < 0){
							newPos.x = newPos.x + (newPos.z-15)*speed;
						}else{
							newPos.x = newPos.x - (newPos.z-15)*speed;
						}
					}else{
						if(newPos.y > 0){
							newPos.x = newPos.x + (newPos.z-15)*speed;
						}else{
							newPos.x = newPos.x - (newPos.z-15)*speed;
						}
					}
				}
				newPos.x += speed2*10 + 50 - 25 * (j%7);
				if(j%7%2==1){
					newPos.y += 37.5 - 25 * (j/7);
				}else{
					newPos.y += 50 - 25 * (j/7);
				}
				if(newPos.x>50||newPos.x<-50){
					alphaGS=2.0;
				}else{
					alphaGS=1.0;
				}
				worldPos = M * vec4(newPos, 1.0);
				gl_Position = V * worldPos;
				gl_Position = P * gl_Position;

				fragposGS = vec3(worldPos);
				normalGS = normalize(gs_in[i].normal);
				texCoordGS = gs_in[i].texCoord;
				EmitVertex();  
			}
			EndPrimitive();
		}
	}else{
		alphaGS=1.0;
		for (int i = 0; i < gl_in.length(); ++i) {
			vec3 newPos=gs_in[i].bPos;
			if(mode == 1){
				if(newPos.z < 10){
					newPos.z = newPos.z * 3;
				}else if(newPos.x + newPos.z > 39){
					if(newPos.x + newPos.z > 51){
						newPos.z = newPos.z + 34.2;
					}else{
						newPos.z = (newPos.z-(39-newPos.x)) + newPos.z + 19;
					}
				}else{
					newPos.z = newPos.z + 19;
				}
			}else if(mode == 2){
				if( newPos.z < 15){
					if(newPos.x < 0){
						if(newPos.y < 0){
							newPos.x = newPos.x + (newPos.z-15)*speed;
						}else{
							newPos.x = newPos.x - (newPos.z-15)*speed;
						}
					}else{
						if(newPos.y > 0){
							newPos.x = newPos.x + (newPos.z-15)*speed;
						}else{
							newPos.x = newPos.x - (newPos.z-15)*speed;
						}
					}
				}
			}else if(mode == 3){
				newspeed=(speed+speed3)/2;
				if(newPos.z < 22 && newPos.x > -23){
					if(newPos.x < 0){
						if(newPos.y < 0){
							newPos.x = newPos.x + (newPos.z-22)*speed3*3;
						}else{
							newPos.x = newPos.x + (newPos.z-22)*speed*3;
						}
					}else{
						if(newPos.y > 0){
							newPos.x = newPos.x - (newPos.z-22)*speed3*3;
						}else{
							newPos.x = newPos.x - (newPos.z-22)*speed*3;
						}
					}
					if(newspeed < 0){
						newPos.z = newPos.z*(1+newspeed*2);
					}else{
						newPos.z = newPos.z*(1-newspeed*2);
					}
				}else{
					if(newspeed < 0){
						newPos.z = newPos.z+newspeed*40;
					}else{
						newPos.z = newPos.z-newspeed*40;
					}
				}
			}
			worldPos = M * vec4(newPos, 1.0);
			gl_Position = V * worldPos;
			gl_Position = P * gl_Position;

			fragposGS = vec3(worldPos);
			normalGS = normalize(gs_in[i].normal);
			texCoordGS = gs_in[i].texCoord;
			EmitVertex();  
			}
		EndPrimitive();
	}
}
