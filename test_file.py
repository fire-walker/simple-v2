# lthing = ['first', 'second', 'third']

# # lthing[0] = lthing[0] + ' active'

# # print(lthing)

# if 'first' in lthing:
#     print(True)
# else:
#     print(False)
# from werkzeug.security import generate_password_hash, check_password_hash

# # print(generate_password_hash('somepass'))
# if check_password_hash('pbkdf2:sha256:150000$shDSqMo1$9b7b3b4cbf65d9add0a8a4ed78dd9ed22ba9dc78d9d2f7208b73dca445df935c', 'somepass'):
#     print(True)
# else:
#     print(False)

# class User():
#     id = 'someid'
#     isauth = True
    
# # print(User.id)
# post_data = {
#     1 : {'title': 'the title',
#          'desc': 'the desc',
#          'content': ['the first para is this <:mother--www.google.com:> fucker. <~This~> isnt <**over**> you <*know*>', '<media--somevideo.mp4>', '<media--someimg.jpg>', '<-this is `the` code->']},
#     2 : 'somethingelse man',
#     3 : 'just osmething mate'
# }


# # post = {x:y for x, y in post_data.items() if x == int(2)}

# # # print(post[0].title)
# # print(list(post.keys())[0])

# # thing = 'j'

# # if thing == '':
# #     print(False)
# # else:
# #     print(True)






# for para_num, para in enumerate(post_data[1]['content']):
#     if para.startswith('<-') and para.endswith('->'):
#         para = para.replace('<-', '').replace('->', '')
#         words = para.split(' ')
#         for word_num, word in enumerate(words):
#             if word.startswith('`') and word.endswith('`'):
#                 word = word.replace('`', '')
#                 output = f"<span class='code-box-special'>{word}</span>"
#                 words[word_num] = output
                
#         para = f"<code>{' '.join(words)}</code>"
    
#     elif para.startswith('<media--') and para.endswith('>'):
#         para = para.replace('<', '').replace('>', '')
#         media_file = para.split('--')[1]
        
#         image_prefixes = ('.png', '.jpg', '.jpeg')
#         if media_file.endswith(image_prefixes):
#             para = f"<img src='{{{{ url_for('static/media', '{media_file}') }}}}'>"
#         else:
#             para = f"<video controls><source src='{{{{ url_for('static/media', '{media_file}') }}}}' type='video/{media_file.split('.')[-1]}'>"
    
#     else:
#         words = para.split(' ')
#         for word_num, word in enumerate(words):
#             # links
#             if word.startswith('<:') and word.endswith(':>'):
#                 word = word.replace('<:', '').replace(':>', '')
#                 elements = word.split('--')
#                 output = f"<a class='link' href='{elements[1]}'>{elements[0]}</a>"

#             # code snippets
#             elif word.startswith('<~') and word.endswith('~>'):
#                 word = word.replace('<~', '').replace('~>', '')
#                 output = f"<code class='code-snippet'>{word}</code>"
                
#             # bold
#             elif word.startswith('<**') and word.endswith('**>'):
#                 word = word.replace('<**', '').replace('**>', '')
#                 output = f"<b>{word}</b>"

#             # italic
#             elif word.startswith('<*') and word.endswith('*>'):
#                 word = word.replace('<*', '').replace('*>', '')
#                 output = f"<i>{word}</i>"
                
#             else:
#                 continue

#             words[word_num] = output
            
#         para = f"<p>{' '.join(words)}</p>"
    
#     post_data[1]['content'][para_num] = para


# for i in post_data[1]['content']:
#     print(i)
    
    
    
    
n = 0
for i in range(5):
    n += 1
    print(n)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
