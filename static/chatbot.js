(function() {
    // Message constructor
    var Message = function(args) {
        this.text = args.text;
        this.messageSide = args.message_side;

        // Draw method to display the message
        this.draw = (function(_this) {
            return function() {
                var $message;
                // Clone the message template and update the content
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.messageSide).find('.text').html(_this.text);
                $('.messages').append($message);

                // Add 'appeared' class with a delay for animation effect
                setTimeout(function() {
                    $message.addClass('appeared');
                }, 0);
            };
        })(this);

        return this;
    };

    $(function() {
        // Function to get the text from the input field
        var getMessageText = function() {
            return $('.message_input').val();
        };

        // Function to send a message
        var sendMessage = function(text) {
            if (text.trim() === '') {
                return;
            }

            // Clear the input field
            $('.message_input').val('');
            var $messages = $('.messages');
            var messageSide = 'right';

            // Create and draw the user message
            var userMessage = new Message({
                text: text,
                message_side: messageSide
            });
            userMessage.draw();

            // AJAX call to send message to the server and get the response
            $.ajax({
                type: 'POST',
                url: '/chat',
                contentType: 'application/json',
                data: JSON.stringify({ message: text }),
                success: function(data) {
                    // Create and draw the bot response message
                    var botMessage = new Message({
                        text: data.response,
                        message_side: 'left'
                    });
                    botMessage.draw();
                    // Scroll to the bottom of the messages
                    $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
                },
                error: function() {
                    // Create and draw an error message
                    var errorMessage = new Message({
                        text: "Sorry, there was an error processing your message.",
                        message_side: 'left'
                    });
                    errorMessage.draw();
                    // Scroll to the bottom of the messages
                    $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
                }
            });

            // Scroll to the bottom of the messages
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };

        // Event handler for send button click
        $('.send_message').click(function() {
            sendMessage(getMessageText());
        });

        // Event handler for Enter key press in input field
        $('.message_input').keyup(function(e) {
            if (e.which === 13) {
                sendMessage(getMessageText());
            }
        });

        // Add an initial welcome message
        var welcomeMessage = new Message({
            text: "Hello! I am a chatbot designed to provide information about the ongoing Israel-Palestine conflict. How can I assist you today?",
            message_side: 'left'
        });
        welcomeMessage.draw();
    });
}).call(this);
