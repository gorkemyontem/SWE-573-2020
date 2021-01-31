var render = (template, selector) => {
    var node = document.querySelector(selector);
    if (!node) return;
    node.innerHTML = template;
};

var mediaTemplate = (mediaArr) => {
    templates = mediaArr.map(
        (media) => `
    <li class="media sa-media-parent" id="submission-${media.id}">
        <a class="mr-3" target="_blank" href="${addRedditBaseUrl(media.permalink)}">
            <img src="${findImage(media.url, media.permalink)}" class="img-small img-thumbnail mr-3">
        </a>
        <div class="media-body">
            <h5 class="mt-0 mb-2" title="${getTitle('title')}">${media.title}</h5>
            <div class="icon-set">
                <a class="mr-3" target="_blank" href="${addRedditBaseUrl(media.permalink)}">
                    <span class="sa-link" title="${getTitle('id')}">#${media.submission_id}</span>
                </a>
                <span title="${getTitle('date')}"><i class="fas fa-calendar-day"></i>&nbsp;${dateFormat(media.created_utc)}</span>
            </div>
            <div class="icon-set">
                <span title="${getTitle('score')}"><i class="fas fa-star"></i>&nbsp;${media.score}</span>
                <span title="${getTitle('polarity')}"><i class="fas fa-flag"></i>&nbsp;${round(media.polarity)}</span>
                <span title="${getTitle('avg_polarity')}"><i class="far fa-circle"></i>&nbsp;${round(media.avg_polarity)}</span>
                <span title="${getTitle('classification')}">&nbsp;${classify(media.classification)}</span>
                <span title="${getTitle('subjectivity')}"><i class="fas fa-head-side-cough"></i>&nbsp;${round(media.subjectivity)}</span>
                <span title="${getTitle('num_comments')}"><i class="fas fa-list-ol"></i>&nbsp;${media.num_comments}</span>
            </div>
            <p class="sa-media-content">${media.selftext.substring(0, 500) + '...'}</p>
            <div class="clearfix">
                <button type="button" class="btn btn-sm btn-primary shadow p-2 px-3 float-right" data-toggle="collapse" data-target="#collapse-${media.id}">
                    Show Top 10 Comments
                </button>
                <button type="button" class="btn btn-sm btn-primary shadow p-2 px-3 mr-2 float-right" id="btn-${media.id}" onclick="triggerPopup('${media.id}','${media.submission_id}', 'sentences_submissions')">
                    Show Sentence Analysis and Entities
                </button>
            </div>
            <div class="sa-media-children">
                <div class="collapse" id="collapse-${media.id}">
                    <div class="card card-body">
                        ${mediaChildrenTemplate(media.children)}
                    </div>
                </div>


            </div>
        </div>
    </li>`
    );
    return `<ul class="list-unstyled">${templates.join('')}</ul>`;
};

var mediaChildrenTemplate = (children) => {
    templates = children.map(
        (media) => `
    <div class="media mt-3" id="comment-${media.id}">
        <div class="media-body">
                <div class="icon-set">
                    <a class="mr-3" target="_blank" href="${addRedditBaseUrl(media.permalink)}">
                        <span class="sa-link" title="${getTitle('id')}">#${media.comment_id}</span>
                    </a>
                    <span title="${getTitle('date')}"><i class="fas fa-calendar-day"></i>&nbsp;${dateFormat(media.created_utc)}</span>
                </div>
                <div class="icon-set">
                    <span title="${getTitle('score')}"><i class="fas fa-star"></i>&nbsp;${media.score}</span>
                    <span title="${getTitle('polarity')}"><i class="fas fa-flag"></i>&nbsp;${round(media.polarity)}</span>
                    <span title="${getTitle('avg_polarity')}"><i class="far fa-circle"></i>&nbsp;${round(media.avg_polarity)}</span>
                    <span title="${getTitle('classification')}">&nbsp;${classify(media.classification)}</span>
                    <span title="${getTitle('subjectivity')}"><i class="fas fa-head-side-cough"></i>&nbsp;${round(media.subjectivity)}</span>
                    <span title="${getTitle('depth')}"><i class="fas fa-level-down-alt"></i>&nbsp;${media.depth}</span>
                </div>
            <p class="sa-media-content">${media.body}</p>
            <div class="clearfix">
                <button type="button" class="btn btn-sm btn-primary shadow p-2 px-3 float-right" id="btn-${media.id}" onclick="triggerPopup('${media.id}','${media.comment_id}', 'sentences_comments')">
                    Show Sentence Analysis and Entities
                </button>
            </div>
        </div>
    </div>`
    );
    return templates.join('');
};

var tableRowTemplate = (data) => {
    templates = data.map(
        (el) => `
    <tr>
        <td title="${getTitle('sentence')}">&nbsp;${el.text}</td>
        <td title="${getTitle('polarity')}">${round(el.polarity)}</td>
        <td title="${getTitle('classification')}">${classify(el.classification)}</td>
        <td title="${getTitle('subjectivity')}">${round(el.subjectivity)}</td>
        <td title="${getTitle('noun_phrases')}">${el.noun_phrases}</td>
        <td title="${getTitle('words')}">${el.words}</td>
        <td title="${getTitle('entities')}">${entities(el.entities)}&nbsp;</td>
    </tr>
    `
    );
    return templates.join('');
};

var titleMap = {
    id: 'Reddit ID',
    title: 'Submission Title',
    sentence: 'Sentence',
    score: 'Reddit Score',
    num_comments: 'Number of Comments',
    depth: 'Comment Depth Level',
    subjectivity: 'Textblob Subjectivity Rate',
    polarity: 'Textblob Polarity Rate',
    avg_polarity: 'Average of Each Sentences Polarity Rate',
    classification: 'Polarity Classification',
    date: 'Created Date',
    link: 'Reddit Permalink',
    noun_phrases: 'Noun Phrases',
    words: 'Words',
    entities: 'Entities',
};

var addRedditBaseUrl = (permalink) => 'https://reddit.com' + permalink;
var findImage = (url, permalink) => (permalink.slice(permalink.length - 25) != url.slice(url.length - 25) && url.slice(url.length - 4).includes('.') ? url : 'https://via.placeholder.com/150');
var dateFormat = (date) => moment(date).format('DD.MM.YYYY HH:mm');
var round = (num) => Math.round(num * 100) / 100;
var classify = (classification) => (classification == 'Positive' ? '<i class="text-success far fa-smile"></i>' : classification == 'Negative' ? '<i class="text-danger far fa-frown"></i>' : '<i class="text-warning far fa-meh"></i>');
var getTitle = (title) => titleMap[title];
var entities = (entity) => {
    let re = /title:(.*?),/g;
    entity = entity.replace(re, 'title:$1 <a href="http://en.wikipedia.org/wiki/$1" target="_blank"><i class="fas fa-external-link-alt"></i></a>,');
    entity = entity.replaceAll('[', '[ ');
    entity = entity.replaceAll(']', ' ]');
    entity = entity.replaceAll('spot:', '<strong>');
    entity = entity.replaceAll(', title:', '</strong> => ');
    entity = entity.replaceAll(', title:', '</strong> => ');
    return entity.split('|').join('<br>');
};

var insertAfter = (referenceNode, newNode) => referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);

var triggerPopup = (id, reddit_id, type) => {
    const btn = document.querySelector('#btn-' + id);
    popup = createPopup(id);
    insertAfter(btn, popup);
    openPopup(id);
    fetchData(type, reddit_id).then((res) => {
        const body = document.querySelector('.popup-body');
        body.innerHTML = `
                        <table class="table table-striped">
                        <thead>
                            <tr>
                                <th style="width: 25%">&nbsp;Sentence</th>
                                <th style="width: 5%">Polarity</th>
                                <th style="width: 5%">Classification</th>
                                <th style="width: 5%">Subjectivity</th>
                                <th style="width: 12%">Noun_phrases</th>
                                <th style="width: 16%">Words</th>
                                <th style="width: 32%">Entities</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableRowTemplate(res)}
                        </tbody>
                        </table>
                        `;
    });
};

var createPopup = (id) => {
    var element = document.createElement('div');
    element.classList.add('popup-modal', 'shadow');
    element.setAttribute('id', 'popup-' + id);
    element.innerHTML = `<i class="fas fa-2x fa-times text-white bg-primary p-3 popup-modal__close"></i><h1 class="font-weight-bold">Sentence Analysis</h1><div class="popup-body"></div>`;
    return element;
};

var openPopup = (id) => {
    const popup = document.querySelector('#popup-' + id);
    popup.classList.add('is--visible');
    popup.querySelector('.popup-modal__close').addEventListener('click', () => {
        closePopup(id);
    });

    const bodyBlackout = document.querySelector('.body-blackout');
    bodyBlackout.classList.add('is-blacked-out');
    bodyBlackout.addEventListener('click', () => {
        closePopup(id);
    });
};

var closePopup = (id) => {
    const popup = document.querySelector('#popup-' + id);
    popup.remove();
    const bodyBlackout = document.querySelector('.body-blackout');
    bodyBlackout.classList.remove('is-blacked-out');
};

var fetchData = (type, id) =>
    fetch(requestBase(`/api/ajax/${type}/${id}/`), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body) {
                return;
            }
            if (body && body.data && body.data.sentenceAnalysis) {
                return body.data.sentenceAnalysis;
            }
        });
