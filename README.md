# AI Digital Human Education Video Generator (Feasibility Version)

## 项目简介
AI数字人教育视频生成器是一款专为教育领域设计的智能视频生成平台，能够将文本内容快速转换为带有AI数字人讲解的教学视频。该平台集成了大语言模型、语音合成和数字人生成技术，帮助教育工作者和机构高效创建高质量的教学资源。

## 核心功能

### 1. 多模态教学内容创作
- 支持语音/文本双模式输入，灵活创建教学内容
- 实时智能转换，将输入内容优化为适合演讲的脚本
- 可视化教学逻辑编辑器，支持内容结构调整

### 2. 智能教学内容优化
- 基于教育心理学原理优化内容表达
- LLM教学化微调，确保内容专业且易于理解
- 个性化适配算法，根据不同学科和受众调整内容风格

### 3. 个性化数字人教师
- 多风格教师形象库，满足不同教学场景需求
- 自然情感表达，提升教学感染力
- 多语言支持，实现跨语言教学

### 4. 灵活的教学视频布局
- 多场景教学模板（黑板、PPT、场景化等）
- 智能元素编排，自动调整文字、图像、数字人位置
- 多平台适配，支持横屏/竖屏等不同格式

## 技术栈

### 前端
- Vue.js 3
- Vite
- Axios

### 后端
- Python 3.9+
- Flask
- OpenAI SDK (用于豆包大模型)
- Volcengine SDK (用于数字人生成)
- MoviePy (视频处理)
- Pillow (图像处理)

### 核心服务
- 豆包大模型 (文本优化)
- 火山引擎数字人平台 (数字人生成)
- 火山引擎语音合成 (TTS)

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 14+
- npm 6+

### 安装与启动

#### Mac/Linux
```bash
git clone <repository-url>
cd ai_people
chmod +x start.sh
./start.sh
```

#### Windows
```bash
git clone <repository-url>
cd ai_people
double click start.bat
```

### 手动启动（可选）

#### 1. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python run.py
```

#### 2. 启动前端服务
```bash
cd frontend
npm install
npm run dev
```

## 访问方式
- 前端界面：http://localhost:3000
- 后端API：http://localhost:5000

## 详细配置

配置文件位于 backend/app/config.py，包含以下核心配置项：

### 1. 火山引擎配置
```python
VOLC_ACCESS_KEY = "YOUR_VOLC_ACCESS_KEY"
VOLC_SECRET_KEY = "YOUR_VOLC_SECRET_KEY"
RESOURCE_ID = "250623-zhibo-linyunzhi"
```

### 2. 豆包大模型配置
```python
ARK_API_KEY = "YOUR_ARK_API_KEY"
DOUBAO_MODEL_ID = "doubao-seed-1-6-251015"
```

### 3. 大模型响应配置
```python
LLM_MAX_RESPONSE_LENGTH = 1000
```

### 4. 演示模式配置
```python
DEMO_MODE = False
DEMO_VIDEO_PATH = ""
DEMO_AUDIO_PATH = ""
DEMO_DELAY_SECONDS = 10
DEMO_TEXT = ""
```

## 使用指南

### 1. 基本使用流程
1. 访问前端界面 http://localhost:3000
2. 在输入框中输入教学内容
3. 选择数字人形象和语音风格
4. 选择视频布局模板
5. 点击生成视频按钮
6. 等待视频生成完成
7. 预览和下载生成的教学视频

### 2. 高级功能
- 内容优化：系统会自动将输入内容优化为适合演讲的脚本
- 布局调整：支持自定义数字人位置、大小和背景
- 批量生成：支持批量输入多个教学内容，自动生成多个视频

## 项目结构

```
ai_people/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── service/
│   │   │   ├── llm_service.py
│   │   │   ├── tts_service.py
│   │   │   ├── volc_service.py
│   │   │   └── video_service.py
│   │   ├── app.py
│   │   └── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── temp/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── PROJECT_INTRO.md
├── README.md
├── start.sh
└── start.bat
```

## API文档

### 1. 生成视频
- URL: /api/generate_video
- Method: POST
- Request Body:
  ```json
  {
    "text": "教学内容文本",
    "voice": "zh-CN-XiaoxiaoNeural",
    "layout": "raw",
    "max_length": 1000
  }
  ```
- Response:
  ```json
  {
    "taskId": "uuid-string"
  }
  ```

### 2. 查询任务状态
- URL: /api/task_status/<task_id>
- Method: GET
- Response:
  ```json
  {
    "taskId": "uuid-string",
    "progress": 50,
    "videoUrl": "",
    "status": "processing",
    "text": "原始文本",
    "voice": "zh-CN-XiaoxiaoNeural",
    "layout": "raw"
  }
  ```

## 开发指南

### 1. 后端开发
- 开发环境：Python 3.9+
- 依赖管理：pip
- 运行测试：python -m pytest
- 代码风格：PEP 8

### 2. 前端开发
- 开发环境：Node.js 14+
- 依赖管理：npm
- 开发模式：npm run dev
- 构建生产版本：npm run build

## 注意事项

1. API密钥安全
   - 请勿将包含真实API密钥的配置文件提交到版本控制系统
   - 建议使用环境变量管理敏感信息

2. 性能优化
   - 视频生成过程可能需要较长时间
   - 建议将大文件处理任务放在后台进行

3. 浏览器兼容性
   - 建议使用Chrome、Firefox等现代浏览器
   - 部分功能可能在IE浏览器中不可用

4. 资源限制
   - 免费版API可能有调用次数限制
   - 生成的视频文件会占用临时存储空间，请定期清理

## 故障排除

### 1. 视频生成失败
- 检查API密钥是否正确配置
- 检查网络连接是否正常
- 查看后端日志获取详细错误信息

### 2. 前端无法访问后端
- 检查后端服务是否正常运行
- 检查跨域配置是否正确

### 3. 数字人不显示
- 确保已正确配置火山引擎API密钥
- 检查RESOURCE_ID是否有效

## 未来计划

1. 增加更多数字人形象和语音风格
2. 支持自定义数字人外观
3. 增加字幕自动生成功能
4. 支持多语言教学视频生成
5. 集成更多教育资源模板
6. 支持视频编辑和后期处理

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目地址：https://github.com/your-username/ai-digital-human-education
- 邮箱：your-email@example.com

版本信息：Feasibility Version 1.0
最后更新：2024年1月
