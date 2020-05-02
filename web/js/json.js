function ArticleStatistics(url, task, specifiedTask, result) {
    this.url = url;
    this.task = task;
    this.specifiedTask = specifiedTask;
    this.words = [];

    let words = getResultAttribute(result, task, 'phrases').flat(Infinity);
    let pos = getResultAttribute(result, task, 'pos').flat(Infinity);
    let dep = getResultAttribute(result, task, 'pos').flat(Infinity);

    if (words.length === pos.length && words.length === dep.length) {
        for (let i = 0; i < words.length; i++) {
            this.words.push(
                {
                    value : words[i],
                    correct : 0,
                    wrong : 0,
                    pos : pos[i],
                    dep : dep[i],
                }
            )
        }
    } else {
        console.log('Wrong result parameter');
    }
};

ArticleStatistics.prototype.toJson = function () {
    return {
        url : this.url,
        exercise : [{
            task : this.task,
            specifiedTask : this.specifiedTask,
            words : this.words,
        }],
    };
};
