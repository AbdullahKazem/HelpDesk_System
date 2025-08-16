window.botpress.on("webchat:ready", () => {
    window.botpress.open();
  });
window.botpress.init({
    "botId": "4c2de288-faeb-4c34-829c-fc021c1ec7f7",
    "configuration": {
      "version": "v1",
      "botName": "EgyptAir Support",
      "botDescription": "I can help you to solve any tech problem in English or Arabic.",
      "website": {},
      "email": {},
      "phone": {},
      "termsOfService": {},
      "privacyPolicy": {},
      "color": "#183B4E",
      "variant": "solid",
      "headerVariant": "glass",
      "themeMode": "light",
      "fontFamily": "inter",
      "radius": 4,
      "feedbackEnabled": true,
      "footer": "[EgyptAir Customer Support](https://www.egyptair.com)"
    },
    "clientId": "f80fb28b-43eb-4f0c-801c-2c4e5e9c1770",
    "selector": "#webchat"
  });