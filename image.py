import logging
import imgkit
import os


def get_html(user, to_give):
    '''Returns beautiful html for email'''
    logging.info('get_html()')
    html = '''
            <!DOCTYPE html>
            <html>
            <body>
            <div style="padding:20px 0px; text-align:center;">
                <img src="https://act4.tv/wp-content/uploads/2020/11/SecretSanta-500.jpg" style="height: 300px;">
                <h3>Secret Santa</h3>
                <p>Hi {}</p>
                <p>Your Secret Santa is:</p>
                <h2>{}<h2>
                <h3>Rules</h3>
                <ul style="text-align: center; list-style-position: inside;">
                    <li>You cannot spend more than £8</li>
                    <li>Please remember to keep this a secret</p>
                </ul>
            </div>
            </body>
            </html>
        
        '''.format(user, to_give)
    return html

def get_image(user, to_give):
    html = get_html(user, to_give)
    options = {
        'format': 'jpg',
        'encoding': "UTF-8",
    }
    try:
        filename = 'images/{}.html'.format(user)
        outname = 'images/{}.jpg'.format(user)
        file = open(filename, "w")
        file.write(html)
        file.close()
        imgkit.from_file(filename, outname, options=options)
        os.remove(filename)
    except OSError as error:
        logging.error('Error writing file: {}'.format(error))