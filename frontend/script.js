// DOM Elements
const textInput = document.getElementById('text-input');
const checkBtn = document.getElementById('check-btn');
const resultsChartCtx = document.getElementById('results-chart').getContext('2d');
const verdictText = document.getElementById('verdict-text');
const heroTitle = document.getElementById('hero-title');
const heroDesc = document.getElementById('hero-desc');
const navHome = document.getElementById('nav-home');
const navAbout = document.getElementById('nav-about');
const navLearn = document.getElementById('nav-learn');
const dialectBtns = document.querySelectorAll('.dialect-btn');
const languageToggleBtns = document.querySelectorAll('.language-toggle-btn');
const aboutTitle = document.getElementById('about-title');
const aboutDesc = document.getElementById('about-desc');
const techTitle = document.getElementById('tech-title');
const learnTitle = document.getElementById('learn-title');
const learnSub1 = document.getElementById('learn-sub1');
const learnText1 = document.getElementById('learn-text1');
const learnSub2 = document.getElementById('learn-sub2');
const learnText2 = document.getElementById('learn-text2');
const copyrightText = document.getElementById('copyright-text');
const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
const hamburger = document.getElementById("hamburger-btn");
const mobileMenu = document.querySelector(".mobile-menu");

// Initialize Chart
let resultsChart = new Chart(resultsChartCtx, {
  type: 'doughnut',
  data: {
    labels: ['كلام مسيء', 'كلام عادي'],
    datasets: [{
      data: [0, 100],
      backgroundColor: ['#FF4D4D', '#4CAF50'],
      borderWidth: 0
    }]
  },
  options: {
    cutout: '70%',
    plugins: { legend: { display: false } },
    animation: { animateScale: true, animateRotate: true },
    elements: { arc: { borderWidth: 2, borderColor: '#1A1A1A' } }
  }
});

// Initialize Mobile Menu
function initMobileMenu() {
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
  });

  mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('active');
      hamburger.classList.remove('active');
      document.body.style.overflow = '';

      // Update active state
      mobileNavLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });
}

// Initialize Language Toggle
function initLanguageToggle() {
  if (!languageToggleBtns.length) return;

  const translations = {
    'hero-title': {
      ar: 'كفى: اكتشف الكلام المسيء في اللغة العربية',
      en: 'Kaffah: Detect Hate Speech in Arabic'
    },
    'hero-desc': {
      ar: 'أدخل النص في المربع أدناه لتحليل ما إذا كان يحتوي على كلام مسيء أو كراهية. اختر اللهجة أولاً (العربية الفصحى أو الجزائرية).',
      en: 'Enter text in the box below to analyze if it contains offensive or hate speech. First select the dialect (Modern Standard Arabic or Algerian).'
    },
    'text-input': {
      placeholder: {
        ar: 'اكتب النص هنا...',
        en: 'Type your text here...'
      },
      listening: {
        ar: 'جاري الاستماع...',
        en: 'Listening...'
      }
    },
    'voice-btn': {
    title: {
      ar: 'إدخال صوتي',
      en: 'Voice Input'
    }
  },
  'file-input': {
    title: {
      ar: 'تحميل ملف',
      en: 'Upload File'
    }
  },
  'voice-status': {
    ar: 'جاري التسجيل... اضغط للتوقف',
    en: 'Recording... Click to stop'
  },
  'image-placeholder': {
    ar: '[صورة - يتطلب معالجة OCR لاستخراج النص]',
    en: '[Image - OCR processing required to extract text]'
  },
   
    'check-btn': {
      ar: 'تحليل',
      en: 'Analyze'
    },
    'verdict-text': {
      ar: 'نتيجة التحليل تظهر هنا',
      en: 'Analysis results will appear here'
    },
    'msa-dialect': {
      ar: 'العربية الفصحى',
      en: 'Modern Standard Arabic'
    },
    'darija-dialect': {
      ar: 'اللهجة الجزائرية',
      en: 'Algerian Dialect'
    },
    'about-title': {
      ar: 'عن المشروع',
      en: 'About the Project'
    },
    'about-desc': {
      ar: '"كفى" هو منصة ذكاء اصطناعي متقدمة تستخدم نماذج معالجة اللغة الطبيعية (NLP) لاكتشاف الكلام المسيء والتحريضي في النصوص العربية، بما في ذلك اللهجة الجزائرية. يعتمد النظام على تقنيات مثل AraBERT و Farasa لتحليل النصوص بدقة.',
      en: '"Kaffah" is an advanced AI platform that uses Natural Language Processing (NLP) models to detect offensive and inflammatory speech in Arabic texts, including the Algerian dialect. The system relies on technologies like AraBERT and Farasa for accurate text analysis.'
    },
    'tech-title': {
      ar: 'التقنيات المستخدمة:',
      en: 'Technologies Used:'
    },
    'learn-title': {
      ar: 'لماذا مكافحة خطاب الكراهية؟',
      en: 'Why Combat Hate Speech?'
    },
    'learn-sub1': {
      ar: 'خطورة خطاب الكراهية',
      en: 'The Danger of Hate Speech'
    },
    'learn-text1': {
      ar: 'خطاب الكراهية يهدد تماسك المجتمعات ويؤدي إلى التمييز والعنف. يمكن أن يتسبب في انقسامات عميقة وتهميش لفئات كاملة من الناس.',
      en: 'Hate speech threatens social cohesion and leads to discrimination and violence. It can cause deep divisions and marginalization of entire groups of people.'
    },
    'learn-sub2': {
      ar: 'دورنا في المواجهة',
      en: 'Our Role in Confrontation'
    },
    'learn-text2': {
      ar: 'نقدم أدوات تقنية لاكتشاف الكلام المسيء، لأن الكشف المبكر يساعد في الحد من انتشاره ويحمي ضحاياه المحتملين.',
      en: 'We provide technical tools to detect offensive speech, because early detection helps limit its spread and protects potential victims.'
    },
    'copyright-text': {
      ar: '© 2025 كفى - جميع الحقوق محفوظة',
      en: '© 2025 Kaffah - All Rights Reserved'
    },
    'nav-home': {
      ar: 'الرئيسية',
      en: 'Home'
    },
    'nav-about': {
      ar: 'عن المشروع',
      en: 'About'
    },
    'nav-learn': {
      ar: 'تعلم المزيد',
      en: 'Learn'
    },
    'mobile-nav-home': {
      ar: 'الرئيسية',
      en: 'Home'
    },
    'mobile-nav-about': {
      ar: 'عن المشروع',
      en: 'About'
    },
    'mobile-nav-learn': {
      ar: 'تعلم المزيد',
      en: 'Learn'
    },
    'tech-item-1': {
      ar: 'نماذج Transformers (مثل AraBERT)',
      en: 'Transformer Models (e.g., AraBERT)'
    },
    'tech-item-2': {
      ar: 'مكتبة Hugging Face',
      en: 'Hugging Face Library'
    },
    'tech-item-3': {
      ar: 'معالجة اللهجات العربية (الفصحى والجزائرية)',
      en: 'Arabic Dialect Processing (MSA & Algerian)'
    },
    'dialect-btn-msa': {
    ar: 'العربية الفصحى',
    en: 'Modern Standard Arabic'
  },
  'dialect-btn-darija': {
    ar: 'اللهجة الجزائرية',
    en: 'Algerian Dialect'
  },
  };

  function updateLanguage(lang) {
    document.documentElement.lang = lang;
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
  
  

    Object.entries(translations).forEach(([id, texts]) => {
      const element = document.getElementById(id);
      if (element) {
        if (id === 'text-input') {
          element.placeholder = texts.placeholder[lang];
        } else {
          element.textContent = texts[lang];
        }
      }
    });
  
    resultsChart.data.labels = lang === 'ar' ? ['كلام مسيء', 'كلام عادي'] : ['Hate Speech', 'Normal'];
    resultsChart.update();
    localStorage.setItem('preferredLanguage', lang);
    restoreVoiceIcon();


  }
  function restoreVoiceIcon() {
    const voiceBtn = document.getElementById('voice-btn');
    if (voiceBtn && !voiceBtn.querySelector('i.fa-microphone')) {
      voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    }
  }
  languageToggleBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const lang = this.dataset.lang;
      updateLanguage(lang);
      languageToggleBtns.forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
    });
  });

  const preferredLanguage = localStorage.getItem('preferredLanguage') || 'ar';
  document.querySelector(`.language-toggle-btn[data-lang="${preferredLanguage}"]`).classList.add('active');
  updateLanguage(preferredLanguage);
}


// Initialize Dialect Toggle
function initDialectToggle() {
  dialectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      dialectBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
}

// Initialize Smooth Scrolling
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        const headerHeight = document.querySelector('nav').offsetHeight;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });

        document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
          link.classList.remove('active');
        });
        this.classList.add('active');
      }
    });
  });
}

// Initialize Analysis
function initAnalysis() {
  checkBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    if (!text) return;
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.detail || "Prediction failed");
      }
      
      const isHate = result.is_hate_speech;
      // Important change: Interpret confidence based on what class was detected
      const confidence = result.confidence;
      let hatePercent, notHatePercent;
      
      if (isHate) {
        // If hate speech, confidence is the hate speech percentage
        hatePercent = confidence;
        notHatePercent = 100 - confidence;
      } else {
        // If not hate speech, confidence is the not-hate speech percentage
        notHatePercent = confidence;
        hatePercent = 100 - confidence;
      }
      
      // Set dynamic labels, colors, and data for the chart
      let labels, colors, data;
      if (isHate) {
        labels = ['Hate Speech', 'Not Hate'];
        colors = ['#FF4D4D', '#E0E0E0'];
        data = [hatePercent, notHatePercent];
      } else {
        labels = ['Not Hate', 'Hate Speech'];
        colors = ['#4CAF50', '#E0E0E0'];
        data = [notHatePercent, hatePercent];
      }
      // Update the chart with the new data
      resultsChart.data.labels = labels;
      resultsChart.data.datasets[0].backgroundColor = colors;
      resultsChart.data.datasets[0].data = data;
      resultsChart.update();
      
      // Prepare the result text to display the verdict
      const lang = document.documentElement.lang;
      let verdictMessage = "";
      if (lang === 'ar') {
        // Arabic verdict message
        verdictMessage = isHate
          ? `كلام مسيء (${hatePercent.toFixed(1)}%)`
          : `كلام عادي (${notHatePercent.toFixed(1)}%)`;
        if (isHate && result.category) {
          verdictMessage += ` - التصنيف: ${result.category}`;
        }
      } else {
        // English verdict message
        verdictMessage = isHate
          ? `Hate Speech (${hatePercent.toFixed(1)}%)`
          : `Normal Speech (${notHatePercent.toFixed(1)}%)`;
        if (isHate && result.category) {
          verdictMessage += ` - Category: ${result.category}`;
        }
      }
      
      // Set the verdict text and color based on whether it's hate speech or not
      verdictText.textContent = verdictMessage;
      verdictText.style.color = isHate ? '#FF4D4D' : '#4CAF50';
    } catch (err) {
      console.error("Error:", err);
      verdictText.textContent = "⚠️ Prediction failed. Please try again.";
      verdictText.style.color = '#FF4D4D';
    }
  });
}

function updateActiveSectionOnScroll() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
  const scrollPosition = window.scrollY + 100; // Adjust offset as needed
  const documentHeight = document.documentElement.scrollHeight;
  const windowHeight = window.innerHeight;

  // Special handling for when we're at the bottom of the page
  if (scrollPosition + windowHeight >= documentHeight - 100) {
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#learn-section') {
        link.classList.add('active');
      }
    });
    return;
  }

  // Regular section handling
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');

    if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}
// Voice recognition variables
let recognition;
let isRecording = false;

// Initialize voice recognition with cross-browser support
function initVoiceRecognition() {
  const voiceBtn = document.getElementById('voice-btn');
  const voiceStatus = document.getElementById('voice-status');
  const textInput = document.getElementById('text-input');


  const micIcon = document.createElement('i');
  micIcon.className = 'fas fa-microphone permanent-icon';
  voiceBtn.innerHTML = '';
  voiceBtn.appendChild(micIcon);
  // Always show the button (we'll style it differently if unsupported)
  voiceBtn.style.display = 'flex';
  
  // 1. Check for browser support (all prefixes)
  const SpeechRecognition = window.SpeechRecognition || 
                          window.webkitSpeechRecognition || 
                          window.mozSpeechRecognition || 
                          window.msSpeechRecognition;

  if (!SpeechRecognition) {
    markAsUnsupported(voiceBtn);
    return;
  }

  // 2. Initialize recognition
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = document.documentElement.lang === 'ar' ? 'ar-SA' : 'en-US';

  // 3. Event handlers
  recognition.onstart = function() {
    isRecording = true;
    voiceBtn.classList.add('recording');
    voiceStatus.style.display = 'block';
    textInput.placeholder = document.documentElement.lang === 'ar' ? 
      'جاري الاستماع...' : 'Listening...';
  };

  recognition.onerror = function(event) {
    console.error('Voice recognition error:', event.error);
    stopRecording();
    showError(event.error);
  };

  recognition.onend = function() {
    if (isRecording) { // Only stop if not manually stopped
      stopRecording();
    }
  };

  recognition.onresult = function(event) {
    let transcript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        transcript += event.results[i][0].transcript;
      }
    }
    if (transcript) {
      textInput.value = transcript;
    }
  };

  // 4. Button click handler
  voiceBtn.addEventListener('click', function() {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  });

  // 5. Helper functions
  function startRecording() {
    try {
      recognition.start();
    } catch (error) {
      console.error('Error starting recognition:', error);
      voiceStatus.textContent = document.documentElement.lang === 'ar' ?
        'لا يمكن بدء التسجيل' : 'Cannot start recording';
      voiceStatus.style.display = 'block';
    }
  }

  function stopRecording() {
    isRecording = false;
    try {
      recognition.stop();
    } catch (e) {
      console.log('Error stopping:', e);
    }
    voiceBtn.classList.remove('recording');
    voiceStatus.style.display = 'none';
    updatePlaceholder();
  }

  function showError(error) {
    const errors = {
      'no-speech': document.documentElement.lang === 'ar' ? 
        'لم يتم اكتشاف كلام' : 'No speech detected',
      'audio-capture': document.documentElement.lang === 'ar' ?
        'لا يمكن الوصول إلى الميكروفون' : 'Microphone not available',
      'not-allowed': document.documentElement.lang === 'ar' ?
        'تم رفض إذن الميكروفون' : 'Microphone permission denied'
    };
    
    voiceStatus.textContent = errors[error] || 
      (document.documentElement.lang === 'ar' ? 
       'خطأ في التعرف الصوتي' : 'Voice recognition error');
    voiceStatus.style.display = 'block';
  }

  function updatePlaceholder() {
    textInput.placeholder = document.documentElement.lang === 'ar' ?
      'اكتب النص هنا...' : 'Type your text here...';
  }
}

// Mark button as unsupported
function markAsUnsupported(button) {
  button.disabled = true;
  button.style.opacity = '0.5';
  button.style.cursor = 'not-allowed';
  button.title = document.documentElement.lang === 'ar' ?
    'المتصفح لا يدعم التعرف الصوتي' : 
    'Voice input not supported in this browser';
  
  // Optional: Add warning icon
  const warningIcon = document.createElement('span');
  warningIcon.innerHTML = ' ⚠';
  warningIcon.style.color = '#ff0000';
  button.appendChild(warningIcon);
}
// Handle file uploads
function initFileUpload() {
  const fileInput = document.getElementById('file-input');
  const textInput = document.getElementById('text-input');

  fileInput.addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Show loading state
    const lang = document.documentElement.lang;
    textInput.value = lang === 'ar' ? 'جاري معالجة الملف...' : 'Processing file...';

    try {
      if (file.type.startsWith('image/')) {
        // Send image to backend OCR
        const result = await sendToBackendOCR(file);
        textInput.value = result.text || (lang === 'ar' ? 
          'لا يمكن قراءة النص في الصورة' : 'Could not read text from image');
      } else {
        // Handle text files directly
        const text = await readTextFile(file);
        textInput.value = text;
      }
    } catch (error) {
      console.error('File processing error:', error);
      textInput.value = lang === 'ar' ? 
        'خطأ في معالجة الملف' : 'File processing error';
    }
  });
}

// Send image to Python backend OCR endpoint
async function sendToBackendOCR(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile); // Ensure the key is "file"

  try {
    const response = await fetch('http://localhost:8000/ocr', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Server returned an error');
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending to backend:', error);
    throw error; // Re-throw to handle in UI
  }
}


document.addEventListener('DOMContentLoaded', () => {
  // Initialize theme first to prevent flash of wrong theme
  initThemeToggle();
  
  // Then initialize everything else
  initMobileMenu();
  initLanguageToggle();
  initDialectToggle();
  initSmoothScrolling();
  initAnalysis();
  initVoiceRecognition();
  initFileUpload();
  
  // Set active nav items
  document.querySelector('.nav-link[href="#home"]')?.classList.add('active');
  document.querySelector('.mobile-nav-link[href="#home"]')?.classList.add('active');
  
  // Scroll handler
  window.addEventListener('scroll', updateActiveSectionOnScroll);
});

// Add this new function
function initThemeToggle() {
  const themeToggle = document.getElementById('theme-toggle');
  const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
  
  // Set initial theme from localStorage or default to dark
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  // Update all icons and text
  updateThemeUI(savedTheme);
  
  // Desktop toggle handler
  themeToggle?.addEventListener('click', toggleTheme);
  
  // Mobile toggle handler
  mobileThemeToggle?.addEventListener('click', toggleTheme);
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  // Update theme
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  // Update UI
  updateThemeUI(newTheme);
}

function updateThemeUI(theme) {
  const isLight = theme === 'light';
  const icons = document.querySelectorAll('.theme-icon');
  const themeTexts = document.querySelectorAll('.theme-text');
  
  // Update all icons
  icons.forEach(icon => {
    icon.classList.toggle('fa-moon', !isLight);
    icon.classList.toggle('fa-sun', isLight);
  });
  
  // Update all text labels
  themeTexts.forEach(text => {
    text.textContent = isLight ? 'Light Mode' : 'Dark Mode';
  });
}

// OCR File Processing Function
async function sendToOCR(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:8000/ocr', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'OCR request failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('OCR Error:', error);
    return { 
      status: 'error',
      text: 'فشل تحليل الملف', // "File analysis failed" in Arabic
      error: error.message
    };
  }
}

// Connect to your existing file input
document.getElementById('file-input').addEventListener('change', async (e) => {
  if (!e.target.files || e.target.files.length === 0) {
    return;
  }
  
  const file = e.target.files[0];
  
  // Show loading indicator
  const textInput = document.getElementById('text-input');
  textInput.value = 'جاري معالجة الملف...'; // "Processing file..." in Arabic
  
  // Check file type
  const fileType = file.type;
  console.log(`Processing file: ${file.name} (${fileType})`);
  
  // Process the file
  const result = await sendToOCR(file);
  
  // Update the text area with the extracted text
  textInput.value = result.text;
});
















































// DOM Elements for Hate Speech Detection

const viewMoreBtn = document.getElementById('view-more-btn');
const popup = document.getElementById('details-popup');
const closeBtn = document.querySelector('.close-btn');
const classificationDetails = document.getElementById('classification-details');

// Hate Speech Categories Data with Full Details
const hateSpeechCategories = {
  "lgbtq_hate": {
    name: "كراهية مجتمع الميم",
    description: "أي كلام يحض على الكراهية أو العنف أو التمييز ضد أفراد مجتمع الميم (المثليين، المثليات، ثنائيي الجنس، المتحولين جنسيًا).",
    image: "https://img.freepik.com/free-vector/homophobia-illustration-concept_23-2148576276.jpg",
    examples: {
      original: "هذا الشاذ يجب أن يُعاقب",
      translation: "This abnormal should be punished",
      transliteration: "hdha alshadh yjb an yُ'aqb"
    },
    targetedGroup: "أفراد مجتمع الميم (LGBTQ+)",
    indicativePhrases: [
      {
        phrase: "شاذ",
        explanation: "مصطلح تحقيري لأفراد مجتمع الميم"
      },
      {
        phrase: "يجب أن يُعاقب",
        explanation: "تحريض على العنف ضد الفئة المستهدفة"
      }
    ]
  },
  "racism": {
    name: "عنصرية",
    description: "الكلام الذي يحط من قيمة أو يميز ضد شخص أو مجموعة بناءً على العرق أو اللون أو الأصل العرقي.",
    image :'https://img.freepik.com/free-vector/people-protesting-with-stop-racism-message_23-2148611347.jpg',
    examples: {
      original: "هؤلاء الزنوج لا يستحقون العيش بيننا",
      translation: "These blacks don't deserve to live among us",
      transliteration: "ha'ula' alznwj la ysthwqwn al'aysh bynna"
    },
    targetedGroup: "أفراد من أعراق أو أصول معينة",
    indicativePhrases: [
      {
        phrase: "زنوج",
        explanation: "مصطلح عنصري مهين"
      },
      {
        phrase: "لا يستحقون العيش بيننا",
        explanation: "تحريض على التمييز العنصري"
      }
    ]
  },
  // Add other categories with same structure...
};



// Get random main hate type for testing
function getRandomMainHateType() {
  const types = Object.keys(hateSpeechCategories);
  const randomType = types[Math.floor(Math.random() * types.length)];
  return {
    type: randomType,
    ...hateSpeechCategories[randomType]
  };
}

// Show Detailed Hate Speech Report
function showHateSpeechReport(mainType) {
  const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
  
  classificationDetails.innerHTML = `
    <div class="report-header" style="display: flex; align-items: center; gap: 15px;">
      <img src="${mainType.image}" alt="${mainType.name}" style="width: 60px; height: 60px; object-fit: contain;">
      <h3 style="margin: 0; color: ${isDarkMode ? '#f7fafc' : '#1a202c'}">تقرير تحليل خطاب الكراهية</h3>
    </div>
    
    <div class="report-section" style="margin-top: 20px; padding: 15px; border-radius: 8px; background: ${isDarkMode ? '#4a5568' : '#f8f9fa'};">
      <div class="report-row" style="margin-bottom: 12px;">
        <span class="report-label" style="font-weight: bold; color: ${isDarkMode ? '#cbd5e0' : '#4a5568'}; min-width: 120px; display: inline-block;">النص الأصلي:</span>
        <p class="report-content arabic-text" style="display: inline; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">${mainType.examples.original}</p>
      </div>
      
      <div class="report-row" style="margin-bottom: 12px;">
        <span class="report-label" style="font-weight: bold; color: ${isDarkMode ? '#cbd5e0' : '#4a5568'}; min-width: 120px; display: inline-block;">الترجمة:</span>
        <p class="report-content" style="display: inline; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">${mainType.examples.translation}</p>
      </div>
      
      <div class="report-row" style="margin-bottom: 12px;">
        <span class="report-label" style="font-weight: bold; color: ${isDarkMode ? '#cbd5e0' : '#4a5568'}; min-width: 120px; display: inline-block;">نوع الخطاب:</span>
        <p class="report-content category-badge" style="display: inline; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">${mainType.name}</p>
      </div>
      
      <div class="report-row" style="margin-bottom: 12px;">
        <span class="report-label" style="font-weight: bold; color: ${isDarkMode ? '#cbd5e0' : '#4a5568'}; min-width: 120px; display: inline-block;">الفئة المستهدفة:</span>
        <p class="report-content" style="display: inline; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">${mainType.targetedGroup}</p>
      </div>
      
      <div class="phrases-section" style="margin-top: 15px;">
        <h4 style="color: ${isDarkMode ? '#f7fafc' : '#1a202c'}; margin-bottom: 10px;">العبارات الدالة:</h4>
        ${mainType.indicativePhrases.map(phrase => `
          <div class="phrase-item" style="margin-bottom: 10px;">
            <span class="phrase-text" style="font-weight: bold; color: #d32f2f;">"${phrase.phrase}"</span>
            <span class="phrase-explanation" style="color: ${isDarkMode ? '#cbd5e0' : '#4a5568'}; margin-right: 5px;">
              ${phrase.explanation}
            </span>
          </div>
        `).join('')}
      </div>
    </div>
    
    <div class="education-section" style="margin-top: 20px; padding: 15px; border-radius: 8px; background: ${isDarkMode ? '#4a5568' : '#f8f9fa'};">
      <h4 style="margin-top: 0; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">معلومات عن "${mainType.name}"</h4>
      <p style="line-height: 1.6; color: ${isDarkMode ? '#f7fafc' : '#1a202c'};">${mainType.description}</p>
    </div>
  `;
  
  popup.style.display = 'block';
  updatePopupTheme(); // Apply current theme
}

// Add this to your theme toggle function
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  updateThemeUI(newTheme);
  updatePopupTheme(); // Update popup when theme changes
}

// Initialize with theme support
document.addEventListener('DOMContentLoaded', () => {
  // ... your existing initialization code ...
  
  // Watch for theme changes
  const observer = new MutationObserver(updatePopupTheme);
  observer.observe(document.documentElement, { 
    attributes: true, 
    attributeFilter: ['data-theme'] 
  });
})

// Simulate Analysis (Temporary Testing)
function simulateAnalysis() {
  const mainType = getRandomMainHateType();
  const hatePercent = Math.floor(Math.random() * 50) + 50; // 50-100%
  
  // Update chart
  resultsChart.data.datasets[0].data = [hatePercent, 100 - hatePercent];
  resultsChart.update();
  
  // Update verdict text
  verdictText.textContent = `${hatePercent}% ${mainType.name}`;
  verdictText.style.color = '#FF4D4D';
  
  // Show view more button
  viewMoreBtn.style.display = 'block';
  
  // Store for detailed view
  window.mainHateType = mainType;
}

// Event Listeners
checkBtn.addEventListener('click', () => {
  const text = textInput.value.trim();
  if (!text) {
    alert("الرجاء إدخال نص للتحليل");
    return;
  }
  
  // Simulate analysis
  checkBtn.disabled = true;
  checkBtn.textContent = "جاري التحليل...";
  
  setTimeout(() => {
    simulateAnalysis();
    checkBtn.disabled = false;
    checkBtn.textContent = "تحليل";
  }, 1500);
});

viewMoreBtn.addEventListener('click', () => {
  if (window.mainHateType) {
    showHateSpeechReport(window.mainHateType);
  } else {
    alert("لا توجد نتائج متاحة لعرض التفاصيل");
  }
});

closeBtn.addEventListener('click', () => popup.style.display = 'none');
window.addEventListener('click', (e) => {
  if (e.target === popup) popup.style.display = 'none';
});



function updatePopupTheme() {
  const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
  const popupContent = document.querySelector('.popup-content');
  
  if (popupContent) {
    if (isDarkMode) {
      // Dark mode styles
      popupContent.style.backgroundColor = '#2d3748';
      popupContent.style.color = '#f7fafc';
      popupContent.querySelectorAll('.report-section, .education-section').forEach(section => {
        section.style.backgroundColor = '#4a5568';
        section.style.color = '#f7fafc';
      });
      popupContent.querySelectorAll('.report-label, .phrase-explanation').forEach(el => {
        el.style.color = '#cbd5e0';
      });
    } else {
      // Light mode styles
      popupContent.style.backgroundColor = '#fefefe';
      popupContent.style.color = '#1a202c';
      popupContent.querySelectorAll('.report-section, .education-section').forEach(section => {
        section.style.backgroundColor = '#f8f9fa';
        section.style.color = '#1a202c';
      });
      popupContent.querySelectorAll('.report-label, .phrase-explanation').forEach(el => {
        el.style.color = '#4a5568';
      });
    }
  }
}

// Initialize other components...
initMobileMenu();
initLanguageToggle();
// ... other init functions