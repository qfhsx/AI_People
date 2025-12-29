<template>
  <div class="h5-container">
    <!-- Background Video Players (Dual Buffering) -->
    <video 
      ref="player1"
      class="bg-video"
      :class="{ active: activePlayer === 1 }"
      :src="player1Src"
      autoplay
      playsinline
      :loop="player1Loop"
      :muted="isMuted"
      @ended="onVideoEnded(1)"
      @playing="onVideoPlay(1)"
      @click="toggleMute"
    ></video>
    
    <video 
      ref="player2"
      class="bg-video"
      :class="{ active: activePlayer === 2 }"
      :src="player2Src"
      autoplay
      playsinline
      :loop="player2Loop"
      :muted="isMuted"
      @ended="onVideoEnded(2)"
      @playing="onVideoPlay(2)"
      @click="toggleMute"
    ></video>

    <!-- Settings Button (Floating) -->
    <div class="settings-btn" @click="showSettings = true">
      <el-icon :size="24" color="#fff"><Setting /></el-icon>
    </div>

    <!-- Subtitle Overlay -->
    <transition name="fade">
      <div v-if="currentSubtitle" class="subtitle-overlay">
        {{ currentSubtitle }}
      </div>
    </transition>

    <!-- Main Interaction Area -->
    <div class="interaction-area">
       <!-- Status Text -->
       <transition name="fade">
         <div v-if="statusText" class="status-text">{{ statusText }}</div>
       </transition>
       
       <div class="input-controls">
         <!-- Mode Switcher -->
          <div class="mode-switch-btn" @click="toggleInputMode">
            <el-icon :size="24" color="#fff" v-if="inputMode === 'voice'"><Edit /></el-icon>
            <el-icon :size="24" color="#fff" v-else><Microphone /></el-icon>
          </div>

         <!-- Voice Input Mode -->
         <template v-if="inputMode === 'voice'">
           <div 
             class="record-btn" 
             :class="{ 'recording': isRecording, 'loading': isLoading }"
             @click="handleRecordClick"
           >
             <div class="record-icon">
                <el-icon :size="40" v-if="isLoading" class="is-loading"><Loading /></el-icon>
                <el-icon :size="40" v-else-if="isRecording"><Microphone /></el-icon>
                <el-icon :size="40" v-else><Microphone /></el-icon>
             </div>
             <div class="ripple" v-if="isRecording"></div>
           </div>
         </template>

         <!-- Text Input Mode -->
         <div v-else class="text-input-container">
           <el-input 
             v-model="textInput" 
             placeholder="Type a message..." 
             class="text-input-field"
             @keyup.enter="handleTextSubmit"
             :disabled="isLoading"
           >
             <template #append>
               <el-button @click="handleTextSubmit" :loading="isLoading">
                 <el-icon><Position /></el-icon>
               </el-button>
             </template>
           </el-input>
         </div>

         <!-- Spacer to balance layout if needed, or keep empty -->
         <div class="spacer"></div>
       </div>

       <div class="hint-text" v-if="inputMode === 'voice' && !isRecording && !isLoading">Tap to Speak</div>
    </div>

    <!-- Settings Drawer -->
    <el-drawer 
      v-model="showSettings" 
      title="Settings" 
      direction="btt" 
      size="60%"
      :show-close="false"
      class="settings-drawer"
    >
      <el-form :model="form" label-position="top">
        <el-form-item label="Digital Human">
           <el-tag>250623-zhibo-linyunzhi</el-tag>
        </el-form-item>
        
        <el-form-item label="Voice Style">
          <el-select v-model="form.voice" placeholder="Select Voice" style="width: 100%">
            <el-option label="Female Teacher (Xiaoxiao)" value="zh-CN-XiaoxiaoNeural" />
            <el-option label="Male Narrator (Yunxi)" value="zh-CN-YunxiNeural" />
            <el-option label="Lively Girl (Xiaoyi)" value="zh-CN-XiaoyiNeural" />
            <el-option label="Steady Male (Yunjian)" value="zh-CN-YunjianNeural" />
            <el-option label="Cute Boy (Yunxia)" value="zh-CN-YunxiaNeural" />
            <el-option label="Cantonese Female (HiuMaan)" value="zh-HK-HiuMaanNeural" />
            <el-option label="Taiwanese Female (HsiaoChen)" value="zh-TW-HsiaoChenNeural" />
          </el-select>
        </el-form-item>

        <el-form-item label="Layout Mode">
          <el-radio-group v-model="form.layout">
            <el-radio label="raw">Full Screen (Raw)</el-radio>
            <el-radio label="merge">Lecture Mode (Merge)</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Setting, Microphone, VideoPause, Loading, Edit, ChatLineRound, Position } from '@element-plus/icons-vue'

// Dual Player Refs
const player1 = ref(null)
const player2 = ref(null)
const activePlayer = ref(1) // 1 or 2
const player1Src = ref('/start.mp4')
const player2Src = ref('')
const player1Loop = ref(false)
const player2Loop = ref(false)

const showSettings = ref(false)
const isRecording = ref(false)
const isLoading = ref(false)
const isMuted = ref(true)
const statusText = ref('')
const currentSubtitle = ref('')
const currentVideoUrl = ref('/start.mp4') // Logical current video
const inputMode = ref('voice')
const textInput = ref('')

// Video Paths
const VIDEO_PATHS = {
  START: '/start.mp4',
  DEFAULT: '/default.mp4',
  DEFAULT_1: '/default_1.mp4',
  THINKING_START: '/thinking_start.mp4',
  THINKING_LOOP: '/thinking.mp4',
  THINKING_END: '/thinking_end.mp4'
}

const form = reactive({
  voice: 'zh-CN-XiaoxiaoNeural',
  layout: 'raw'
})

let recognition = null
let taskId = ''
let pollInterval = null
let pendingResponseVideoUrl = null 
let pendingSubtitleText = ''
let targetSubtitleText = ''
let typewriterInterval = null

// Helper to switch video
const switchVideo = (url, loop = false) => {
    const targetId = activePlayer.value === 1 ? 2 : 1
    const currentPlayer = activePlayer.value === 1 ? player1.value : player2.value
    
    // Pause current to prevent race conditions
    if (currentPlayer) currentPlayer.pause()

    if (targetId === 1) {
        player1Src.value = url
        player1Loop.value = loop
        nextTick(() => {
            if (player1.value) {
                player1.value.load()
                player1.value.play().catch(e => console.error("Play error:", e))
            }
        })
    } else {
        player2Src.value = url
        player2Loop.value = loop
        nextTick(() => {
            if (player2.value) {
                player2.value.load()
                player2.value.play().catch(e => console.error("Play error:", e))
            }
        })
    }
}

// Event Handlers
const onVideoPlay = (id) => {
    if (activePlayer.value !== id) {
        activePlayer.value = id
        currentVideoUrl.value = (id === 1 ? player1Src.value : player2Src.value)
    }

    if (targetSubtitleText && activePlayer.value === id) {
        const player = id === 1 ? player1.value : player2.value
        // Duration might be NaN if not ready, default to estimated duration based on text length
        // Assume roughly 4 chars per second (0.25s per char) if duration unknown
        const duration = (player && player.duration && isFinite(player.duration)) ? player.duration : (targetSubtitleText.length * 0.25)
        startTypewriter(targetSubtitleText, duration)
        targetSubtitleText = ''
    }
}

const startTypewriter = (text, totalDuration) => {
    if (typewriterInterval) clearInterval(typewriterInterval)
    currentSubtitle.value = ''
    if (!text) return
    
    // Split text into segments based on punctuation for better readability
    // Matches content followed by punctuation, or remaining content
    const segments = text.match(/[^，。！？；：,.!?\n]+[，。！？；：,.!?\n]?/g) || [text]
    
    const totalLength = text.length
    const startTime = Date.now()
    // Convert duration to ms
    const totalDurationMs = totalDuration * 1000
    
    // Calculate cumulative progress thresholds for each segment
    let accumulatedLen = 0
    const segmentThresholds = segments.map(seg => {
        accumulatedLen += seg.length
        return accumulatedLen / totalLength
    })
    
    typewriterInterval = setInterval(() => {
        const now = Date.now()
        const elapsed = now - startTime
        const progress = elapsed / totalDurationMs
        
        // If finished
        if (progress >= 1) {
             const last = segments[segments.length - 1]
             const prev = segments.length > 1 ? segments[segments.length - 2] : ''
             
             const clean = (s) => s.replace(/[，。！？；：,.!?\n]+$/, '')
             const c = clean(last)
             const p = prev ? clean(prev) : ''
             
             currentSubtitle.value = p ? `${p}\n${c}` : c
             
             clearInterval(typewriterInterval)
             typewriterInterval = null
             return
        }
        
        // Find current segment index based on progress
        let activeIndex = 0
        for (let i = 0; i < segmentThresholds.length; i++) {
            if (progress < segmentThresholds[i]) {
                activeIndex = i
                break
            }
            activeIndex = i
        }
        
        // Show current and previous segment (max 2 lines/segments)
        let currentSeg = segments[activeIndex]
        let prevSeg = activeIndex > 0 ? segments[activeIndex - 1] : ''
        
        // Remove trailing punctuation (user requested to remove symbols at end of line)
        const clean = (s) => s.replace(/[，。！？；：,.!?\n]+$/, '')
        
        currentSeg = clean(currentSeg)
        if (prevSeg) prevSeg = clean(prevSeg)
        
        currentSubtitle.value = prevSeg ? `${prevSeg}\n${currentSeg}` : currentSeg
        
    }, 50)
}

const onVideoEnded = (id) => {
    if (id !== activePlayer.value) return
    
    const current = currentVideoUrl.value
    console.log(`Video ended: ${current}`)

    if (current === VIDEO_PATHS.START) {
        switchVideo(VIDEO_PATHS.DEFAULT, false)
        return
    }

    if (current === VIDEO_PATHS.THINKING_START) {
        if (pendingResponseVideoUrl) {
             switchVideo(VIDEO_PATHS.THINKING_END, false)
        } else {
             switchVideo(VIDEO_PATHS.THINKING_LOOP, true)
        }
        return
    }
    
    if (current === VIDEO_PATHS.THINKING_END) {
        if (pendingResponseVideoUrl) {
            isLoading.value = false
            statusText.value = ""
            const responseUrl = pendingResponseVideoUrl
            const subtitle = pendingSubtitleText
            pendingResponseVideoUrl = null
            pendingSubtitleText = ''
            
            switchVideo(responseUrl, false)
            targetSubtitleText = subtitle
        } else {
            console.warn("thinking_end finished but no response url")
        }
        return
    }
    
    if (current === VIDEO_PATHS.DEFAULT) {
        switchVideo(VIDEO_PATHS.DEFAULT_1, false)
        return
    }
    if (current === VIDEO_PATHS.DEFAULT_1) {
        switchVideo(VIDEO_PATHS.DEFAULT, false)
        return
    }

    console.log("Response video ended. Switching to default.")
    if (typewriterInterval) {
        clearInterval(typewriterInterval)
        typewriterInterval = null
    }
    currentSubtitle.value = ''
    switchVideo(VIDEO_PATHS.DEFAULT, false)
}

onMounted(() => {
  initSpeechRecognition()
  nextTick(() => {
      if (player1.value) {
          player1.value.play().catch(e => {
            console.log("Autoplay blocked", e)
            statusText.value = "Tap to Unmute/Start"
          })
      }
  })
})

const toggleMute = () => {
    isMuted.value = !isMuted.value
    if (!isMuted.value && statusText.value === "Tap to Unmute/Start") {
        statusText.value = ""
        const p = activePlayer.value === 1 ? player1.value : player2.value
        p?.play()
    }
}

const toggleInputMode = () => {
  inputMode.value = inputMode.value === 'voice' ? 'text' : 'voice'
}

const handleTextSubmit = () => {
  if (!textInput.value.trim() || isLoading.value) return
  if (isMuted.value) toggleMute()
  const text = textInput.value
  textInput.value = ''
  submitTask(text)
}

const initSpeechRecognition = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    ElMessage.error('Browser does not support Speech Recognition. Please use Chrome.')
    return
  }
  recognition = new SpeechRecognition()
  recognition.lang = 'zh-CN'
  recognition.continuous = true // Changed to true to allow manual stop
  recognition.interimResults = true // Enable interim results to capture partial speech

  recognition.onstart = () => {
    console.log("Recognition started")
    isRecording.value = true
    statusText.value = "Listening..."
  }
  
  recognition.onaudiostart = () => {
      console.log("Audio capturing started")
  }
  
  recognition.onsoundstart = () => {
      console.log("Sound detected")
  }
  
  recognition.onspeechstart = () => {
      console.log("Speech detected")
  }

  recognition.onnomatch = (event) => {
      console.log("No match found")
      statusText.value = "Didn't catch that. Try again."
  }

  recognition.onend = () => {
    console.log("Recognition ended")
    isRecording.value = false
    // Don't clear status immediately if we have a final result
    if (!isLoading.value && statusText.value === "Listening...") {
        statusText.value = "" 
    }
  }

  recognition.onresult = (event) => {
    console.log("onresult fired. Results length:", event.results.length)
    let finalTranscript = ''
    let interimTranscript = ''

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      const result = event.results[i]
      console.log(`Result [${i}]: isFinal=${result.isFinal}, text="${result[0].transcript}", conf=${result[0].confidence}`)
      
      if (result.isFinal) {
        finalTranscript += result[0].transcript
      } else {
        interimTranscript += result[0].transcript
      }
    }
    
    // Update status with interim results so user sees what's being heard
    if (interimTranscript) {
         statusText.value = `Listening: ${interimTranscript}`
         // Store interim result as potential submission if stopped manually
         recognition.lastInterim = interimTranscript
    }

    if (finalTranscript) {
        console.log("Final result:", finalTranscript)
        statusText.value = `You said: ${finalTranscript}`
        recognition.stop()
        submitTask(finalTranscript)
    } else {
        // Handle case where isFinal=true but text is empty (common in some network/browser failures)
        const hasFinal = Array.from(event.results).some(r => r.isFinal)
        if (hasFinal && !interimTranscript) {
            console.warn("Received final result with empty text.")
            statusText.value = "无法识别，请检查网络或重试 (Unrecognized)"
            
            // If we have a previous interim result that was valid, try to use it
            if (recognition.lastInterim) {
                 console.log("Recovering from last interim:", recognition.lastInterim)
                 finalTranscript = recognition.lastInterim
                 statusText.value = `You said: ${finalTranscript}`
                 recognition.stop()
                 submitTask(finalTranscript)
            }
        }
    }
  }

  recognition.onerror = (event) => {
    console.error('Speech recognition error', event.error)
    
    if (event.error === 'no-speech') {
        console.warn("No speech detected")
        statusText.value = "No speech detected. Check mic."
        // We don't return here anymore so we can see the logic flow
    } 

    if (event.error === 'not-allowed') {
        statusText.value = "Mic Permission Denied"
        ElMessage.error("Microphone access denied. Please check your browser settings.")
    } else if (event.error === 'service-not-allowed') {
        statusText.value = "Service Error"
        ElMessage.error("Speech recognition service not allowed.")
    } else if (event.error === 'network') {
        statusText.value = "Network Error. Switching to text mode..."
        ElMessage.error("无法连接语音服务(需科学上网)。已自动切换为文本输入。")
        // Auto switch to text mode after a short delay so user can continue
        setTimeout(() => {
            if (inputMode.value === 'voice') {
                toggleInputMode()
                statusText.value = "" // Clear error status after switch
            }
        }, 2000)
    } else if (event.error !== 'no-speech') {
        statusText.value = `Error: ${event.error}`
    }
    
    isRecording.value = false
  }
}

const handleRecordClick = () => {
    if (isLoading.value) return
    if (isMuted.value) toggleMute()
    if (isRecording.value) {
        stopRecording()
    } else {
        startRecording()
    }
}

const startRecording = () => {
  if (recognition) {
    console.log("Attempting to start recording...")
    recognition.lastInterim = '' // Reset last interim
    try { 
        recognition.start() 
    } catch(e) { 
        console.error("Start recording error:", e)
        ElMessage.error("Failed to start recording")
    }
  } else {
      ElMessage.error("Speech recognition not supported")
  }
}

const stopRecording = () => {
  if (recognition) {
      recognition.stop()
      // Check if we have any pending interim text to submit
      if (recognition.lastInterim) {
           console.log("Submitting partial result on stop:", recognition.lastInterim)
           statusText.value = `You said: ${recognition.lastInterim}`
           submitTask(recognition.lastInterim)
           recognition.lastInterim = ''
      }
  }
}

const submitTask = async (text) => {
  if (!text || isLoading.value) return
  
  isLoading.value = true
  statusText.value = "Thinking..."
  currentSubtitle.value = ''
  pendingResponseVideoUrl = null
  
  switchVideo(VIDEO_PATHS.THINKING_START, false)
  
  try {
    const res = await axios.post('/api/generate', { 
        text: text,
        voice: form.voice,
        layout: form.layout
    })
    
    if (res.data.code === 200) {
      taskId = res.data.data.taskId
      startPolling()
    } else {
      ElMessage.error(res.data.msg || 'Error submitting')
      isLoading.value = false
      statusText.value = "Error"
    }
  } catch (err) {
    console.error(err)
    ElMessage.error('Network error')
    isLoading.value = false
    statusText.value = "Network Error"
  }
}

const startPolling = () => {
  if (pollInterval) clearInterval(pollInterval)
  
  pollInterval = setInterval(async () => {
    try {
      const res = await axios.get(`/api/status?taskId=${taskId}`)
      if (res.data.code === 200) {
        const data = res.data.data
        
        if (data.status === 'failed') {
          clearInterval(pollInterval)
          isLoading.value = false
          statusText.value = `Error: ${data.msg || 'Task failed'}`
          ElMessage.error(data.msg || 'Task generation failed')
          return
        }

        if (data.videoUrl) {
          clearInterval(pollInterval)
          playResponse(data.videoUrl, data.optimized_text)
        }
      }
    } catch (err) {
      console.error(err)
    }
  }, 2000)
}

const playResponse = (url, text) => {
    pendingResponseVideoUrl = url
    pendingSubtitleText = text
    if (currentVideoUrl.value === VIDEO_PATHS.THINKING_LOOP) {
        switchVideo(VIDEO_PATHS.THINKING_END, false)
    }
}
</script>

<style scoped>
.h5-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #000;
}

.bg-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.bg-video.active {
  z-index: 2;
}

.settings-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
  transition: transform 0.2s;
}

.settings-btn:active {
  transform: scale(0.9);
}

.interaction-area {
  position: absolute;
  bottom: 50px;
  left: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
  padding: 0 20px;
  box-sizing: border-box;
}

.input-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  position: relative;
}

.mode-switch-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 20px;
  transition: transform 0.2s;
}

.mode-switch-btn:active {
  transform: scale(0.9);
}

.text-input-container {
  flex: 1;
  max-width: 300px;
}

.spacer {
  width: 40px; /* Balances the mode switcher width */
  margin-left: 20px;
}

.status-text {
  color: #fff;
  font-size: 16px;
  margin-bottom: 20px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
  background: rgba(0,0,0,0.3);
  padding: 5px 10px;
  border-radius: 20px;
}

.subtitle-overlay {
  position: absolute;
  bottom: 25%;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  max-width: 90%;
  text-align: center;
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  line-height: 1.5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  text-shadow: 0 2px 4px rgba(0,0,0,0.8), 0 0 10px rgba(0,0,0,0.5);
  background: transparent;
  padding: 0;
  z-index: 20;
  pointer-events: none;
  transition: opacity 0.3s ease;
  white-space: pre;
}

.record-btn {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.record-btn:active {
  transform: scale(0.95);
}

.record-btn.recording {
  background: #ff4d4f;
  transform: scale(1.1);
  color: #fff;
}

.record-btn.loading {
    background: #409eff;
    color: #fff;
}

.ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #ff4d4f;
  animation: ripple 1.5s infinite linear;
  opacity: 0;
}

@keyframes ripple {
  0% { width: 100%; height: 100%; opacity: 0.5; }
  100% { width: 200%; height: 200%; opacity: 0; }
}

.hint-text {
  color: rgba(255,255,255,0.7);
  font-size: 12px;
  margin-top: 10px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>