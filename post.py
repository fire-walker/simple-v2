from flask import Flask, render_template, request, Blueprint, Markup
import json

post_blueprint = Blueprint('post_blueprint', __name__)

@post_blueprint.route('/post')
def post():  
    post_id = int(request.args.get('id'))
    
    with open('static/posts.json', "r") as file:
        post_data = {int(x): y for x, y in json.load(file).items()}
 
    if post_id not in post_data:
        return '404', 404
        
    post = {x:y for x, y in post_data.items() if x == post_id}
    
    for para_num, para in enumerate(post[post_id]['content']):
        # codebox
        if para.startswith('<-') and para.endswith('->'):
            para = para.replace('<-', '').replace('->', '')
            words = para.split(' ')
            for word_num, word in enumerate(words):
                if word.startswith('`') and word.endswith('`'):
                    word = word.replace('`', '')
                    output = f"<span class='code-box-special'>{word}</span>"
                    words[word_num] = output
                
                if word == '><':
                    output = '<br>'
                    words[word_num] = output
                    
            para = f"<code>{' '.join(words)}</code>"
        
        # media
        elif para.startswith('<media--') and para.endswith('>'):
            para = para.replace('<', '').replace('>', '')
            media_file = para.split('--')[1]
            
            image_prefixes = ('.png', '.jpg', '.jpeg')
            if media_file.endswith(image_prefixes):
                para = f"<img src='{{{{ url_for('static/media', '{media_file}') }}}}'>"
            else:
                para = f"<video controls><source src='{{{{ url_for('static/media', '{media_file}') }}}}' type='video/{media_file.split('.')[-1]}'>"
        
        # normal para's
        else:
            words = para.split(' ')
            for word_num, word in enumerate(words):
                # links
                if word.startswith('<:') and word.endswith(':>'):
                    word = word.replace('<:', '').replace(':>', '')
                    elements = word.split('--')
                    output = f"<a class='link' href='{elements[1]}'>{elements[0]}</a>"

                # code snippets
                elif word.startswith('<~') and word.endswith('~>'):
                    word = word.replace('<~', '').replace('~>', '')
                    output = f"<span class='code-snippet'>{word}</span>"
                    
                # bold
                elif word.startswith('<**') and word.endswith('**>'):
                    word = word.replace('<**', '').replace('**>', '')
                    output = f"<b>{word}</b>"

                # italic
                elif word.startswith('<*') and word.endswith('*>'):
                    word = word.replace('<*', '').replace('*>', '')
                    output = f"<i>{word}</i>"
                    
                else:
                    continue

                words[word_num] = output
                
            para = f"<p>{' '.join(words)}</p>"
        
        post_data[post_id]['content'][para_num] = Markup(para)
        
    
    return render_template('post.html', page_title='Simple - Post', post=post)
 
        