#version 330 core

uniform sampler2D ourTexture;
uniform float mode;

in vec3 fragposGS;
in vec3 normalGS;
in vec2 texCoordGS;
in float alphaGS;
//in vec3 color;

out vec4 FragColor;

void main()
{
    vec3 furColor = texture(ourTexture, texCoordGS).xyz;
    if(alphaGS==0){
        FragColor = vec4(furColor.x/2, furColor.y/2, furColor.z/2, 1.0);
    }else if(alphaGS==2){
        FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }else {
        FragColor = vec4(furColor, 1.0);
    }
}