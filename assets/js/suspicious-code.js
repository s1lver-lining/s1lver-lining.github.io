async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    return hashBuffer;
}

async function AES_CBC_encrypt(data, key) {

    // Preprare the data
    const algorithm = { name: 'AES-CBC', length: 256 };
    const encodedText = new TextEncoder().encode(data);
    const keyMaterial = await sha256(key);
    const AESkey = await crypto.subtle.importKey('raw', keyMaterial, algorithm, false, ['encrypt']);
  
    // Set the IV to 0x000102030405060708090a0b0c0d0e0f
    const iv = new Uint8Array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]);
  
    // Encrypt the text
    const encryptedBuffer = await crypto.subtle.encrypt({ name: 'AES-CBC', iv: iv }, AESkey, encodedText);
  
    // Combine IV and encrypted data
    const encryptedData = new Uint8Array(iv.byteLength + encryptedBuffer.byteLength);
    encryptedData.set(iv);
    encryptedData.set(new Uint8Array(encryptedBuffer), iv.byteLength);
  
    // Convert to base64
    const encryptedBase64 = btoa(String.fromCharCode.apply(null, encryptedData));
  
    return encryptedBase64;
}

document.addEventListener('DOMContentLoaded', function () {
    function getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }
    
    let p = 197; // Prime number for finite field F_197
    let a, b;
    
    do {
        a = getRandomInt(p);
        b = getRandomInt(p);
    } while ((4 * Math.pow(a, 3, p) + 27 * Math.pow(b, 2, p))%p !== 0);


    let starsContainer = document.querySelector('.stars-container');

    for (let x = 0; x < p; x++) {
        let ySquare = (Math.pow(x, 3) + a * x + b) % p;
        for (let y = 0; y < p; y++) {
            if ((y * y) % p === ySquare) {
                let star = document.createElement('div');
                star.className = 'star bg-black dark:bg-white';
                star.style.top = y + '%';
                star.style.left = x/2 + '%';
                size = 2
                r = Math.random()
                if ( r > 0.7) {
                    size = 1
                }
                if ( r > 0.95) {
                    size = 3
                }
                star.style.width = size + 'px';
                star.style.animationDelay = -Math.random() * 20 + 's';
                star.style.animationDuration = Math.random() * 10 + 10 + 's';
                starsContainer.appendChild(star);
            }
        }
    }
      

    output = `AAECAwQFBgcICQoLDA0OD/LHzij6W72uTzKCLy4tzcjceY+LJ2eA+Hu5JfjmemwWGZHC8aNwDwVsfLQmJUNhFjlakbw4yONsimksNSs3FQ/fo3l4kDZv97F79h5ghaj1vXSzOuyGRFchXHOrKi1LteRkKkj6AYHCBBoxDrtJMMkpmsMMy6lSww0uUM88oKRL+YsFuj2giWRDpqjGnOPmllOMJ+ils8+j8wMxfgnSmCwGrkEBtIJDlSzmp15AnS4qMfD+lmlQ2iUKKsb2q34LdfcUopnnVvAiHKORxEm4/u6WDFyr64q95WShcm2JSkze4mPvqI1MNdbnhFpunPvwGJS+YFsGJShEVSASQ5RFmEFba7gRUi4d4nC3IfMLUmoRI3rGYLAzIJbG5tjX0TgZug1M33PHkHGSKeYI/upJ32cuGqPIQougaRAdczYbm7v0JqAJ9gMW1kbU9utEpiPnZ5mxBjs1YaC+pzUZPfkpoxsMtzxJhmDR+2xiQ6HS0qtrDE69TAK/k0UJaYz5OnIz8zaX2ahrKeGl6IBmPlmJqcKVVfn9acEY8UXwzcRDX/4EbWzc2oks1a1aM8N5r/dtN8XTVpiWvSE14mKk8W8/B7s8sGOwoJXCqi4o/8IQAThtyPq16AZzWhhIdI5kYlU2gCGDRNSwJpgQh27dPJOKaONSyz6zRBD23TK+6MKbBV6BrDZ1jN+kBqR3IJETUwe/v8zbPUNt3Bi8KXqj6+um0VknqXY2BwU+zQxZ7/b1K6wVtkojTLsEbwPXngSy+KIqERF5OaefDBicgYLFi1bk7LkVGJkJ3Zaue537J6SlChyChC2qusf3rmNDgHx8x5e5YyTrK7cdDn1mzCi8Jx8wJOiMxDKMPzCcWgE5YooMx7AVCif6v+g1ncpL5nV3HoXoMvg1OxHMBGfTb/8zmKFWKYgJXojznaMEfxg23MlGVTs3F/ht4Kf2iC50VfZODz7PCSQjDDxLCcUqmiYOjGsx7G8rpcP3E4WnYX+erCarg2jNG2yVeXj9HD4nPKjQJieFO+dDQwmdDGggstZvqDsdghxvp4qXnbLWPl5exeB1U26q9upGZ44jbouSwgUzhxTVp/POxK8uz9DpDLw2duixy00T8e8Ksno50wKdG7wc3BM2e4JSi/h4Qq4x2ao2QT2egYaXVKURn0Oog+OrxIRSC9c=`
    data = `If you pay attention to the stars, you may understand the patterns of the universe`

    async function check_data(a, b, p, data) {

        let key = a.toString() + b.toString() + p.toString()
        if(await AES_CBC_encrypt(data, key) == output) {
            console.log("You found the secret pattern! It was hidden in the stars all along!")
            let new_star = document.createElement('div');
            new_star.className = 'star bg-green-500 dark:bg-green-600';
            new_star.style.top = Math.random() * 100 + '%';
            new_star.style.left = Math.random() * 100 + '%';
            new_star.style.width = '2px';
            new_star.style.animationDelay = -Math.random() * 20 + 's';
            new_star.style.animationDuration = Math.random() * 10 + 10 + 's';
            starsContainer.appendChild(new_star);
        }
    }
    check_data(a, b, p, data)
});