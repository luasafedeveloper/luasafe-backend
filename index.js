const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());

const validKeys = {
    "PREMIUM_KEY_1234": true,
    "MY_FRIEND_KEY": true
};

const coreScript = `
    print("서버로부터 핵심 스크립트를 안전하게 로드했습니다!")

    local Players = game:GetService("Players")
    local localPlayer = Players.LocalPlayer
    print("접속한 플레이어 이름: " .. localPlayer.Name)
`;

app.get('/api/get-script', (req, res) => {
    const userKey = req.query.key;

    if (userKey && validKeys[userKey]) {
        res.send(coreScript);
    } else {
        res.status(403).send("Invalid Key");
    }
});

app.listen(PORT, () => {
    console.log('Luasafe Backend running on port ' + PORT);
});
