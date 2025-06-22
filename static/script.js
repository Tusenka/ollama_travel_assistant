
class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.session_id=crypto.randomUUID();
        this.messages=[]

        this.init();
    }

    init() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.messageInput.addEventListener('input', () => {
            if (this.typingIndicator.classList.contains('visible')) {
                this.hideTypingIndicator();
            }
        });

        // Фокус на поле ввода при загрузке
        this.messageInput.focus();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Очищаем поле ввода
        this.messageInput.value = '';

        this.messages.push({"role": "user", "message:": message});
        // Добавляем сообщение пользователя
        this.addMessage(message, 'user');

        // Показываем индикатор печати
        this.showTypingIndicator();

        console.log('Отправка на сервер ->', { message });

        // Отправляем запрос на сервер
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-ID': this.session_id
                },
                body: JSON.stringify({ messages: this.messages })
            });

            const data = await response.json();

            console.log('Ответ от сервера <-', data);

            // Скрываем индикатор печати
            this.hideTypingIndicator();

            if (data.error) {
                this.addMessage('Извините, произошла ошибка. Попробуйте еще раз.', 'bot');
            } else {
                // Добавляем небольшую задержку для реалистичности
                setTimeout(() => {
                    this.messages.push({"role": "ai", "message": data.reply});
                    this.addMessage(data.reply, 'bot');
                }, 500);
            }
        } catch (error) {
            console.error('Ошибка AJAX запроса:', error);
            this.hideTypingIndicator();
            this.addMessage('Извините, произошла ошибка соединения. Проверьте подключение к интернету.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';

        const icon = document.createElement('i');
        icon.className = sender === 'bot' ? 'fas fa-comment' : 'fas fa-user';
        avatar.appendChild(icon);

        const content = document.createElement('div');
        content.className = 'message-content';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();

        content.appendChild(messageText);
        content.appendChild(messageTime);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        // Добавляем сообщение в чат
        this.chatMessages.appendChild(messageDiv);

        // Прокручиваем к последнему сообщению
        this.scrollToBottom();

        // Добавляем анимацию появления
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';

        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 10);
    }

    showTypingIndicator() {
        this.typingIndicator.classList.add('visible');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.classList.remove('visible');
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    // Метод для добавления анимации загрузки
    addLoadingMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message loading';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';

        const icon = document.createElement('i');
        icon.className = 'fas fa-comment';
        avatar.appendChild(icon);

        const content = document.createElement('div');
        content.className = 'message-content';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = 'Печатает...';

        content.appendChild(messageText);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();

        return messageDiv;
    }


    // Метод для оновления загружающего сообщения
    updateLoadingMessage(messageDiv, text) {
        messageDiv.classList.remove('loading');
        const messageText = messageDiv.querySelector('.message-text');
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        messageDiv.querySelector('.message-content').appendChild(messageTime);
    }
}

// Инициализация чатбота при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Добавляем анимацию для кнопки отправки при наведении
document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendButton');

    sendButton.addEventListener('mouseenter', () => {
        sendButton.style.transform = 'scale(1.05)';
    });

    sendButton.addEventListener('mouseleave', () => {
        sendButton.style.transform = 'scale(1)';
    });

    // Анимация при клике
    sendButton.addEventListener('click', () => {
        sendButton.style.transform = 'scale(0.95)';
        setTimeout(() => {
            sendButton.style.transform = 'scale(1)';
        }, 150);
    });
});

// Добавляем анимацию для поля ввода
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');

    messageInput.addEventListener('focus', () => {
        messageInput.style.transform = 'scale(1.02)';
    });

    messageInput.addEventListener('blur', () => {
        messageInput.style.transform = 'scale(1)';
    });
});

const placeholderTexts = {
    ru: [
        'Посоветуй аппартаменты в Новгороде на 15-20 марта',
        'Покажи свободные аппартаменты на 25-28 декабря в Москве для двоих',
        'Отель в Москве на 5-17 апреля до 40$ в день',
        'Аппартаменты в Ташкенте на сутки'
    ],
    en: [
        'Recommend apartments in Novgorod for March 15–20',
        'Show available apartments in Moscow for two people from December 25–28',
        'A hotel in Moscow from April 5–17 for up to $40 per day',
        'Apartments in Tashkent for one night'
    ],
        en: [
        'Προτείνετε διαμερίσματα στο Νόβγκοροντ για τις 15–20 Μαρτίου',
        'Δείξε διαθέσιμα διαμερίσματα στη Μόσχα για δύο άτομα από 25 έως 28 Δεκεμβρίου',
        'Ξενοδοχείο στη Μόσχα από 5 έως 17 Απριλίου έως 40$ ανά ημέρα',
        'Διαμερίσματα στην Τασκένδη για μία νύχτα'
    ]
};

const userLang = navigator.language.slice(0, 2); // Например, 'ru-RU' → 'ru'

const selectedTexts = placeholderTexts[userLang] || placeholderTexts['en']
let currentIndex = 0;

function changePlaceholder() {
    if (document.getElementById('messageInput')) {
        const placeholderElement = document.getElementById('messageInput');
        placeholderElement.textContent = selectedTexts[currentIndex];
        currentIndex = (currentIndex + 1) % selectedTexts.length;
    }
}
function hintText() {
    if (document.getElementById('messageInput').value.length===0) {
        const placeholderElement = document.getElementById('messageInput');
        placeholderElement.value = selectedTexts[currentIndex];
        currentIndex = (currentIndex + 1) % selectedTexts.length;
    }
}
setInterval(changePlaceholder, 15000);
setInterval(hintText, 8000);
changePlaceholder();
hintText();