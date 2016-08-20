import bs4
import click
import http.client
import logging
import requests
import requests.cookies
import time


http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)
log_url3 = logging.getLogger('requests.packages.urllib3')
log_url3.setLevel(logging.DEBUG)
log_url3.propagate = True

userAgent = "Mozilla/5.0 " \
            "(X11; Linux x86_64) " \
            "AppleWebKit/537.36 " \
            "(KHTML, like Gecko) " \
            "Chrome/52.0.2743.116 " \
            "Safari/537.36"


@click.group()
@click.option('--email', prompt='Amazon email address: ')
@click.option('--password', prompt='Amazon password: ', hide_input=True)
@click.pass_context
def cli(ctx, email, password):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()
    session.headers['User-Agent'] = userAgent
    ctx.obj = {'session': session}

    _login(session, email, password)


def _login(session, email, password):
    login_url = 'https://www.amazon.com/gp/sign-in.html'

    form_response = session.get(login_url)
    print('--- received %s cookies ---' % len(form_response.cookies))
    soup = bs4.BeautifulSoup(form_response.text, 'html5lib')
    form = soup.find('form', {'name': 'signIn'})
    form_action = form['action']
    inputs = form.find_all('input')
    params = {
        i['name']: i['value']
        for i in inputs
        if i.get('type') == 'hidden'
    }
    params['email'] = email
    params['password'] = password

    auth_response = requests.post(form_action, params)
    print('--- received %s cookies ---' % len(auth_response.cookies))
    import pdb; pdb.set_trace()


@cli.command()
def download():
    video_id = '12345'

    main_url = 'https://www.amazon.com/dp/{video_id}/?_encoding=UTF8'
    api_url = 'https://atv-ps.amazon.com/cdp/catalog/GetStreamingUrlSets'


    api_params = {
        'version': 1,
        'format': 'json',
        'firmware': 'WIN 11,7,700,224 PlugIn',
        'marketplaceID': matchMID[0],
        'token': matchToken[0],
        'deviceTypeID': matchDID[0],
        'asin': videoID,
        'customerID': matchCID[0],
        'deviceID': matchCID[0] + str(int(time.time()*1000))+videoID,
    }


if __name__ == '__main__':
    cli()
