document.addEventListener('DOMContentLoaded', function() {
  let questionCount = 0;
  
  function trackQuestions() {
    window.botpressWebChat.onEvent(function(event) {
      if (event.type === 'message' && event.direction === 'outgoing') {
        questionCount++;
        
        if (questionCount >= 3) {
          showSupportButton();
        }
      }
    });
  }

  function showSupportButton() {
    window.botpressWebChat.sendEvent({
      type: 'show_button',
      text: 'Need more help?',
      buttons: [{
        label: 'Contact EgyptAir Support',
        payload: 'redirect_to_support',
        url: 'https://www.egyptair.com/contact'
      }]
    });
  }

  // Wait for Botpress to be ready
  const checkReady = setInterval(() => {
    if (window.botpressWebChat) {
      clearInterval(checkReady);
      trackQuestions();
    }
  }, 100);
});