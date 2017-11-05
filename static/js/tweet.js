function setErrorState(message) {
    const $errorMessage = $('#errorMessage');
    if (!message) {
        $errorMessage.text('');
        $errorMessage.css('display', 'none');
    } else {
        $errorMessage.text(message);
        $errorMessage.css('display', 'block');
    }
}

function onTweetSubmit(event) {
    const tweetText = $('#tweetInput').val();
    if (tweetText.length > 140) {
        setErrorState('Exceeded max length of a tweet.');
        return;
    } else if (tweetText.length == 0) {
        setErrorState('Tweet cannot be empty.');
        return;
    }

    const usernameText = $('#usernameInput').val();
    if (usernameText.length == 0) {
        setErrorState('Username cannot be empty.');
        return;
    }

    Promise.resolve($.get('/api/v1/user/' + usernameText))
    .then(function(res) {
        if (res.error) {
            return Promise.reject(res.error);
        }

        const data = {
            'message': tweetText,
            'author_id': res.user_id
        }

        return Promise.resolve($.post('/api/v1/tweet/', data));
    })
    .then(function(res) {
        if (res.error) {
            return Promise.reject(res.error);
        }

        setErrorState('');
    })
    .catch(function(err) {
        setErrorState(err);
    });
}