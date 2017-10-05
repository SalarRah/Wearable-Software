from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders

#
vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    
    uniform mat4 projection;
    uniform mat4 view;
    uniform mat4 model;
    uniform mat4 transform;

    out vec3 newColor;
    void main() {
        gl_Position =  projection * view * model * transform * vec4(position, 1.0f);
        newColor = color;
    }
    """
    
fragment_shader = """
    #version 330
    in vec3 newColor;
    uniform vec4 setColor;
    layout(location = 0) out vec4 outColor;
    void main()
    {
        outColor = setColor;
    }
    """

    
shader = None

proj_loc = None
view_loc = None
model_loc = None
transform_loc = None
setColor_loc = None




#vertex_shader_texture = """
##version 130
#
#in vec2 vertexpos;
#out vec2 vpos;
#
#void main()
#{
#    vpos = vertexpos;
#    gl_Position = vec4(vertexpos, 0, 1);    
#}"""
#
#fragment_shader_texture = """
##version 130
#
#uniform sampler2D tex;
#in vec2 vpos;
#out vec4 fragColor;
#
#void main ()
#{
#    fragColor = texture2D (tex, (vpos+vec2(1.0, 1.0))*0.5);
#}"""
#
#shader_texture = None
#texture_loc = None