#
# ETNA PROJECT, 12/10/2021 by vast_h
# /home/hugo/Documents/Python
# File description:
#      03-file_handling.py
#
import os
from sys import argv
import paramiko
__author__ = 'vast_h'
__doc__ = 'dsadadas'


def parse_remote_url(remote_url):
    splitted_url = remote_url.split('@')
    if len(splitted_url) != 2:
        return ('erreur', 'erreur')
    username = splitted_url[0]
    host = splitted_url[1]
    return (host, username)


def get_ssh_connection(remote_url):
    (host, username) = parse_remote_url(remote_url)
    if host == 'erreur' and username == 'erreur':
        print('La remote url doit ressembler à username@hostname')
        return 1
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(host, username=username)
        return ssh_client
    except TimeoutError:
        print('Host injoignable')
    return 1


def parse_args():
    """aspdad

    Args:
        parser (as[dksa]): dsadasd
    """
    args = argv[1:]
    if len(args) == 0:
        return ('erreur', [])
    return (args[0], args[1:])


def run_command(ssh_client, command, password=''):
    print('- MY_DEPLOYER BEGIN $ {} '.format(command))
    (stdin, stdout, _) = ssh_client.exec_command(command, get_pty=True)
    stdout.channel.set_combine_stderr(True)
    if command[0:4] == 'sudo':
        stdin.write(password + '\n')
        stdin.flush()

    for line in stdout.readlines():
        print('\t' + line, end='')
    print('- MY_DEPLOYER END $ {} '.format(command))


def config(params):
    if len(params) != 1:
        print("Il manque la remote url")
        return 1
    ssh_client = get_ssh_connection(params[0])
    if ssh_client == 1:
        return
    password = input("Pour le bien des commandes, nous avons besoin de l'accès sudo, merci de bien renseigner le mot de passe\n")
    run_command(ssh_client, 'sudo apt-get update -yq', password)
    run_command(ssh_client, 'sudo apt-get install docker-ce=5:19.03.15~3-0~debian-buster docker-ce-cli=5:19.03.15~3-0~debian-buster containerd.io -yq --allow-downgrades', password)
    run_command(ssh_client, 'docker -v')
    ssh_client.close()


def main():
    """main fucrion

    Returns:
        String: formated output
    """
    (action, params) = parse_args()
    if action == 'config':
        config(params)
    else:
        print('Commande non reconnue ou manquante')


if __name__ == '__main__':
    main()
