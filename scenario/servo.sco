{
  "name": "servo",
  "type": "block",
  "xml": "<block type=\"variables_set\" id=\"318\" inline=\"true\" x=\"293\" y=\"190\"><field name=\"VAR\">pas</field><value name=\"VALUE\"><block type=\"math_number\" id=\"319\"><field name=\"NUM\">10</field></block></value><next><block type=\"variables_set\" id=\"320\" inline=\"true\"><field name=\"VAR\">rotation</field><value name=\"VALUE\"><block type=\"math_number\" id=\"321\"><field name=\"NUM\">0</field></block></value><next><block type=\"setinterval\" id=\"322\" inline=\"true\"><field name=\"handler\">handler</field><comment pinned=\"true\" h=\"113\" w=\"213\">brancher un servo moteur sur la pin digital 10 de l'arduino.\nIci on fait tourner le servo dans un sens puis dans l'autre !</comment><value name=\"time\"><block type=\"math_number\" id=\"323\"><field name=\"NUM\">200</field></block></value><statement name=\"callback\"><block type=\"fwriteservo\" id=\"324\" inline=\"true\"><field name=\"pin\">10</field><value name=\"angle\"><block type=\"variables_get\" id=\"325\"><field name=\"VAR\">rotation</field></block></value><next><block type=\"variables_set\" id=\"326\" inline=\"true\"><field name=\"VAR\">rotation</field><value name=\"VALUE\"><block type=\"math_arithmetic\" id=\"327\" inline=\"true\"><field name=\"OP\">ADD</field><value name=\"A\"><block type=\"variables_get\" id=\"328\"><field name=\"VAR\">rotation</field></block></value><value name=\"B\"><block type=\"variables_get\" id=\"329\"><field name=\"VAR\">pas</field></block></value></block></value><next><block type=\"controls_if\" id=\"330\" inline=\"false\"><mutation elseif=\"1\"></mutation><value name=\"IF0\"><block type=\"logic_compare\" id=\"331\" inline=\"true\"><field name=\"OP\">GT</field><value name=\"A\"><block type=\"variables_get\" id=\"332\"><field name=\"VAR\">rotation</field></block></value><value name=\"B\"><block type=\"math_number\" id=\"333\"><field name=\"NUM\">180</field></block></value></block></value><statement name=\"DO0\"><block type=\"variables_set\" id=\"334\" inline=\"true\"><field name=\"VAR\">pas</field><value name=\"VALUE\"><block type=\"math_number\" id=\"335\"><field name=\"NUM\">-10</field></block></value><next><block type=\"variables_set\" id=\"336\" inline=\"true\"><field name=\"VAR\">rotation</field><value name=\"VALUE\"><block type=\"math_number\" id=\"337\"><field name=\"NUM\">180</field></block></value></block></next></block></statement><value name=\"IF1\"><block type=\"logic_compare\" id=\"338\" inline=\"true\"><field name=\"OP\">LT</field><value name=\"A\"><block type=\"variables_get\" id=\"339\"><field name=\"VAR\">rotation</field></block></value><value name=\"B\"><block type=\"math_number\" id=\"340\"><field name=\"NUM\">0</field></block></value></block></value><statement name=\"DO1\"><block type=\"variables_set\" id=\"341\" inline=\"true\"><field name=\"VAR\">pas</field><value name=\"VALUE\"><block type=\"math_number\" id=\"342\"><field name=\"NUM\">10</field></block></value><next><block type=\"variables_set\" id=\"343\" inline=\"true\"><field name=\"VAR\">rotation</field><value name=\"VALUE\"><block type=\"math_number\" id=\"344\"><field name=\"NUM\">0</field></block></value></block></next></block></statement></block></next></block></next></block></statement></block></next></block></next></block>",
  "codejs": "var pas;\nvar rotation;\nvar handler;\n\n\npas = 10;\nrotation = 0;\n// brancher un servo moteur sur la pin digital 10 de l'arduino.\n// Ici on fait tourner le servo dans un sens puis dans l'autre !\nhandler = setInterval(function(){\n  fwriteServo(10,rotation);rotation = rotation + pas;\n  if (rotation > 180) {\n    pas = -10;\n    rotation = 180;\n  } else if (rotation < 0) {\n    pas = 10;\n    rotation = 0;\n  }\n}\n,200);\n",
  "codepy": ""
}