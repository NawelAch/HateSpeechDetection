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
      }
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
  checkBtn.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (!text) return;

    const dialect = document.querySelector('.dialect-btn.active').dataset.dialect;
    const hatePercent = Math.floor(Math.random() * 100);
    const isHate = hatePercent >= 50;

    resultsChart.data.datasets[0].backgroundColor = isHate ? ['#FF4D4D', '#E0E0E0'] : ['#E0E0E0', '#4CAF50'];
    resultsChart.data.datasets[0].data = [hatePercent, 100 - hatePercent];
    resultsChart.update();

    const lang = document.documentElement.lang;
    verdictText.textContent = lang === 'ar'
      ? isHate ? `كلام مسيء (${hatePercent}%)` : `كلام عادي (${100 - hatePercent}%)`
      : isHate ? `Hate Speech (${hatePercent}%)` : `Normal Speech (${100 - hatePercent}%)`;
    verdictText.style.color = isHate ? '#FF4D4D' : '#4CAF50';
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

// Init Everything
document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initLanguageToggle();
  initDialectToggle();
  initSmoothScrolling();
  initAnalysis();

  document.querySelector('.nav-link[href="#home"]')?.classList.add('active');
  document.querySelector('.mobile-nav-link[href="#home"]')?.classList.add('active');
  window.addEventListener('scroll', updateActiveSectionOnScroll);
});
