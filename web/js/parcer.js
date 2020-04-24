var PARCER_FUNCTIONS = {
    /**
     * Минимальная длина содержимого после тега <body>, которую нельзя игнорировать.
     * @returns {number}
     */
    minBodyTailLength: function() {
        return 100;
    },

    /**
     * Удаляет все что находится за пределами <body> (если существует), а затем удаляет
     * все теги <script>
     * @param html
     * @returns {void | string}
     */
    getStrippedBody: function(html) {
        let body = html.match(/<body[^>]*>(?:([^]*)<\/body>([^]*)|([^]*))/i);
        if (body && body.length > 1) {
            if (body[2] && body[2].length > this.minBodyTailLength()) {
                body = body[1] + ' ' + body[2];
            } else if (body[1] === undefined) {
                body = body[3];
            } else {
                body = body[1];
            }
        } else {
            body = html;
        }

        return body.replace(/<script\b[^>]*(?:>[^]*?<\/script>|\/>)/ig, '<blink/>');
    },

    /**
     * Чистим Html страницу.
     *
     * @param html
     * @param callback
     * @returns {string}
     */
    cleanHtmlPage: function(html, callback) {
        // Выполняем описанную ранее функцию
        html = this.getStrippedBody(html);
        // Удаляем все, кроме текста
        html = html.replace(/<(script|style|object|embed|applet)[^>]*>[^]*?<\/\1>/g, '');
        // // Заменяем теги <img> с источниками, чтобы удалить этот тег без потери изображения.
        // html = html.replace(/<img[^>]*src\s*=\s*['"]?([^<>"' ]+)['"]?[^>]*>/g,
        //     '{startimg:$1:endimg}');
        // Удаляем теги
        html = html.replace(/<[^>]*>/g, '');
        // Сворачиваем пробелы
        html = html.replace(/\s+/g, '');
        // Удаляем номера с общими суффиксами.
        html = html.replace(/\d+ ?(st|nd|rd|th|am|pm|seconds?|minutes?|hours?|days?|weeks?|months?)\b/g, '');
        // Удаляем все кроме букв
        // html = html.replace(/[\x00-\x40\x5B-\x60\x7B-\xBF]/g, '');

        if (callback)
            callback(html);
        else
            return html;
    },

    /**
     * Сравнить две строки
     *
     * @param str1
     * @param str2
     * @returns {number}
     */
    getSimilarity: function(str1, str2) {
        return (new difflib.SequenceMatcher(str1.split(''), str2.split(''))).ratio();
    }
}