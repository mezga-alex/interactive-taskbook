// File to create this kind of JSON file
// JSON = {         // Create inside  createGlobalStatisticsStructure()
//     "statistics": [{    // Create inside createArticleStatisticsStructure()
//         "url": "",
//         "exercises": [{      // Create inside createExerciseStructure()
//             "task" : "",	    // General task type: 'Active, 'Passive'
//             "specification" : [
//                 {
//                     "specifiedTask" : "",		// Specified task: "ALL", "Present Simple" ...
//                     "words": [{                  // Create inside createWordsArrayStructure()
//                         "value": "",             //
//                         "correct": 0,            // Create inside
//                         "wrong": 0,              // createWordStructure()
//                         "pos": "",               //
//                     },]
//                 },
//             ]
//         },
//         ],
//     }],
// }

//
function fetchRequest(data) {
    fetch(server, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            'Access-Control-Allow-Origin': '*',
            "content-type": "application/json"
        })
    })
}

// Update file in database
function updateDataBaseJSON(server, extensionID, json) {
    let data = {extensionID : extensionID,
                json : json};
    fetch(server, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            'Access-Control-Allow-Origin': '*',
            "content-type": "application/json"
        })
    }).then((response) => {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            reject("Error");
        }
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function getDataBaseJSON(server, extensionID) {
    return new Promise((resolve, reject) => {
        let data = {extensionID: extensionID,};
        fetch(server, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(data),
            cache: "no-cache",
            headers: new Headers({
                'Access-Control-Allow-Origin': '*',
                "content-type": "application/json"
            })
        }).then((response) => {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                reject("Error");
            }

            response.json().then((data) => {
                localStorage.setItem('globalStatisticsJSON', JSON.stringify(data));
                resolve('Success');
            });
        }).catch(function (error) {
            console.log("Fetch error: " + error);
            reject("Error")
        });
    });
}

// Single word structure
function createWordStructure(value, pos, dep) {
    return {
        "value": value,
        "correct": 0,
        "wrong": 0,
        "pos": pos,
        "dep": dep,
    }
}

// Array of words structures
function createWordsArrayStructure(wordsData) {
    let values = getResultAttribute(wordsData, task, 'phrases').flat(Infinity);
    let pos = getResultAttribute(wordsData, task, 'pos').flat(Infinity);
    let dep = getResultAttribute(wordsData, task, 'dep').flat(Infinity);

    var words = [];
    if (values.length === pos.length && values.length === dep.length) {
        for (let i = 0; i < values.length; i++) {
            words.push(createWordStructure(values[i], pos[i], dep[i]));
        }
        return words
    } else {
        console.log('Wrong result parameter');
    }
}

function createSpecificationStructure(specifiedTask, words) {
    return {
        "specifiedTask" : specifiedTask,
        "words": words,
    }
}


// Single exercise structure
function createExerciseStructure(task, specifications) {
    if (!specifications.length) specifications = [specifications];

    return {
        "task": task,
        "specifications": specifications,
    }
}

// Array of exercise structures
function createArticleStatisticsStructure(url, exercises) {
    if (!exercises.length) exercises = [exercises];

    return {
        "url": url,
        "exercises": exercises,
    }
}

// Statistics structure
function createGlobalStatisticsStructure(articleStatistics) {
    if (!articleStatistics.length) articleStatistics = [articleStatistics];
    return {
        "statistics": articleStatistics,
    }
}

// Compile full JSON JSON from blocks
function createGlobalJSON(url, task, specifiedTask, result) {
    const words = createWordsArrayStructure(result);
    const specification = createSpecificationStructure(specifiedTask, words);
    const exercise = createExerciseStructure(task, specification);
    const articleStatistics = createArticleStatisticsStructure(url, exercise);
    return createGlobalStatisticsStructure(articleStatistics);
}

// Update JSON structure depending on the task
function updateExerciseNode(globalStatisticsJSON, url, task, specifiedTask, result, isReturnIndices = false) {
    try {
        // Check if we've already updated the structure
        let isUpdated = false;

        // Iterate over unique Article Statistics Nodes (unique URLs)
        for (const [statID, articleStatistics] of globalStatisticsJSON.statistics.entries()) {
            // Check if the user has already worked with the article.
            if (articleStatistics.url === url) {
                // iterate over Article Exercises Nodes
                for (const [exerciseID, exercise] of articleStatistics.exercises.entries()) {
                    if (exercise.task === task) {
                        for (const [specificationID, specification] of exercise.specifications.entries()) {
                            // If there is FULL match -> don't update the structure.
                            if (specification.specifiedTask === specifiedTask) {
                                isUpdated = true;
                                if (isReturnIndices)
                                    return [statID, exerciseID, specificationID];
                                break;      // Not necessary to continue
                            }
                        }

                        if (!isUpdated) {
                            // If there is no FULL match but URL and GENERAL TASK aren't unique ->
                            // push new specification structure to the 'specifications'
                            isUpdated = true;
                            const specificationID = exercise.specifications.length;
                            const words = createWordsArrayStructure(result);
                            const specification = createSpecificationStructure(specifiedTask, words);
                            exercise.specifications.push(specification);
                            if (isReturnIndices)
                                return [statID, exerciseID, specificationID];
                            break;      // Not necessary to continue
                        }
                    }
                }
                if (!isUpdated) {
                    // Add new exercise structure if it's not exist but URL isn't unique
                    isUpdated = true;
                    const exerciseID = articleStatistics.exercises.length;
                    const specificationID = 0;
                    const words = createWordsArrayStructure(result);
                    const specification = createSpecificationStructure(specifiedTask, words);
                    const exercise = createExerciseStructure(task, specification);
                    articleStatistics.exercises.push(exercise);

                    if (isReturnIndices)
                        return [statID, exerciseID, specificationID];
                    break;      // Not necessary to continue
                }
            }
        }

        // If the user hasn't worked with the article before -> create new Article Statistics NODE
        if (!isUpdated) {
            const statID = globalStatisticsJSON.statistics.length;
            const exerciseID = 0;
            const specificationID = 0;

            const words = createWordsArrayStructure(result);
            const specification = createSpecificationStructure(specifiedTask, words);
            const exercise = createExerciseStructure(task, specification);
            const newArticleStatistics = createArticleStatisticsStructure(url, exercise);
            globalStatisticsJSON.statistics.push(newArticleStatistics);
            // console.log('new newArticleStatistics', globalStatisticsJSON.statistics.length, 0);
            // console.log(globalStatisticsJSON);
            if (isReturnIndices)
                return [statID, exerciseID, specificationID];
        }
    } catch (e) {
        alert('ERROR UPDATE');
        console.log('ERROR UPDATE', e);
    }

}

function updateWordStatistics(globalStatisticsJSON, typeOfChange, statID, exerciseID, specificationID, wordID) {
    // Get current word structure
    let word = globalStatisticsJSON.statistics[statID].exercises[exerciseID].specifications[specificationID].words[wordID];
    word[typeOfChange] += 1;
}


$('#resetGlobalStatisticsJSON').on('click', function () {
    localStorage.removeItem('globalStatisticsJSON');
    console.log('reset JSON');
});

$('#logGlobalStatisticsJSON').on('click', function () {
    updateGlobalStatisticsJSON();
    console.log('current JSON status');
    console.log(globalStatisticsJSON);
});

$('#updateDataBaseJSON').on('click', function () {
    console.log('current JSON status');
    console.log(globalStatisticsJSON);
    console.log(extensionID);
    updateDataBaseJSON(server+'/update', extensionID, globalStatisticsJSON);
});

$('#getDataJSON').on('click', function () {
    getDataBaseJSON(server+'/get_data', extensionID);
    globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
    console.log('returned stats from DB');
    console.log(globalStatisticsJSON);
});

// class ArticleExercise {
//     constructor(task, specifiedTask, wordsData) {
//         this.task = task;
//         this.specifiedTask = specifiedTask;
//         try {
//             this.words = JSON.parse(wordsData);
//         } catch (e) {
//             this.words = [];
//             alert(wordsData);
//             let words = getResultAttribute(wordsData, task, 'phrases').flat(Infinity);
//             let pos = getResultAttribute(wordsData, task, 'pos').flat(Infinity);
//             let dep = getResultAttribute(wordsData, task, 'dep').flat(Infinity);
//
//             if (words.length === pos.length && words.length === dep.length) {
//                 for (let i = 0; i < words.length; i++) {
//                     this.words.push(
//                         {
//                             value: words[i],
//                             correct: 0,
//                             wrong: 0,
//                             pos: pos[i],
//                             dep: dep[i],
//                         }
//                     )
//                 }
//             } else {
//                 console.log('Wrong result parameter');
//             }
//         }
//     }
// }
//
// // function ArticleExercise(task, specifiedTask, wordsData) {
// //     this.task = task;
// //     this.specifiedTask = specifiedTask;
// //     try {
// //         this.words = JSON.parse(wordsData);
// //     } catch (e) {
// //         this.words = [];
// //
// //         let words = getResultAttribute(result, task, 'phrases').flat(Infinity);
// //         let pos = getResultAttribute(result, task, 'pos').flat(Infinity);
// //         let dep = getResultAttribute(result, task, 'dep').flat(Infinity);
// //
// //         if (words.length === pos.length && words.length === dep.length) {
// //             for (let i = 0; i < words.length; i++) {
// //                 this.words.push(
// //                     {
// //                         value: words[i],
// //                         correct: 0,
// //                         wrong: 0,
// //                         pos: pos[i],
// //                         dep: dep[i],
// //                     }
// //                 )
// //             }
// //         } else {
// //             console.log('Wrong result parameter');
// //         }
// //     }
// // }
// class ArticleStatistics {
//     constructor(url, task, specifiedTask, wordsData) {
//         this.url = url;
//         this.exercise = new ArticleExercise(task, specifiedTask, wordsData);
//     }
// }
// //
// // function ArticleStatistics(url, articleExerciseData) {
// //     ArticleExercise.call(this);
// //
// //     this.url = url;
// //     // If articleExerciseData is array of 'articleExercise' objects -> copy
// //     if (articleExerciseData.length) {
// //         this.exercise = articleExerciseData
// //     } else {
// //         // If articleExerciseData is a single 'articleExercise' object
// //         this.exercise = [articleExerciseData];
// //     }
// // }
//
// ArticleStatistics.prototype.extractArticleExercise = function (task, specifiedTask) {
//     if (task && specifiedTask) {
//         for (let exercise of this.exercise) {
//             if (exercise.task === task && exercise.specifiedTask === specifiedTask) {
//             }
//         }
//     }
//     return this.exercise;
// };
//
// // Object with full statistics.
// // Structure:
// // statistics : [
// //      {}
// // ]
// class GlobalStatistics {
//     constructor(jsonObj) {
//         try {
//             // The first
//             this.statistics = new ArticleStatistics(jsonObj.url, jsonObj.task, jsonObj.specifiedTask, jsonObj.wordData)
//         } catch () {
//
//         }
//         // this.statistics = new ArticleStatistics(url, task, specifiedTask, wordsData);
//         // if (articleStatisticsData.length) {
//         //     this.statistics = articleStatisticsData
//         // } else {
//         //     // If articleExerciseData is a single 'articleExercise' object
//         //     this.statistics = [articleStatisticsData];
//         // }
//     }
// }
//
// // function GlobalStatistics(articleStatisticsData) {
// //     ArticleStatistics.call(this);
// //     // If articleExerciseData is array of 'articleExercise' objects -> copy
// //     if (articleStatisticsData.length) {
// //         this.statistics = articleStatisticsData
// //     } else {
// //         // If articleExerciseData is a single 'articleExercise' object
// //         this.statistics = [articleStatisticsData];
// //     }
// // }
// //
// // GlobalStatistics.prototype.extractArticleStatistics = function (url) {
// //     if (url) {
// //         for (let articleStatistics of this.statistics) {
// //             if (articleStatistics.url === url) return new ArticleStatistics(url, articleStatistics.exercise)
// //         }
// //     }
// //     return this.statistics;
// // };
//
//
// // ArticleStatistics.prototype.toJson = function () {
// //     return {
// //         url : this.url,
// //         exercise : [{
// //             task : this.task,
// //             specifiedTask : this.specifiedTask,
// //             words : this.words,
// //         }],
// //     };
// // };
//
// // function createArticleExerciseFromJSON(json, url, task, specifiedTask, result) {
// //     try {
// //         json = JSON.parse(json);
// //
// //         if (json.hasOwnProperty('statistics')) {
// //             var isContainURL = false;
// //             for (let articleStatistics of jsonFile.statistics) {
// //                 if (articleStatistics.url === url) {
// //                     isContainURL = true;
// //
// //                     var isContainTask = false;
// //                     for (let exercise of articleStatistics.exercise) {
// //                         // If we already have the same article with the same tasks
// //                         // Restore information about the article statistics with the task from json:
// //                         if (exercise.task === task && exercise.specifiedTask === specifiedTask) {
// //                             isContainTask = true;
// //                             let articleExercise = new ArticleExercise(exercise.task, exercise.specifiedTask, exercise.words);
// //                         }
// //                     }
// //
// //                     // If we already have the URL but for another tasks:
// //                     if (!isContainTask) {
// //                         return new ArticleExercise(task, specifiedTask, result);
// //                     }
// //                 }
// //             }
// //
// //             // If we haven't processed the article yet:
// //             if (!isContainURL) {
// //                 let articleExercise = new ArticleExercise(task, specifiedTask, result);
// //             }
// //         }
// //     } catch (e) {
// //         console.log('Incorrect input data')
// //     }
// // }
// //
// // function globalJSON() {
// //     var GS = {statistics: [],};
// //     gs.statistics.push(articleStatistics)
// // }
// //
// // function updateArticleStatistics() {
// //
// // }
// //
// // function updateGlobalJSON() {
// //
// }