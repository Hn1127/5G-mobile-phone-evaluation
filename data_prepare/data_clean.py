import json
import os

CommentPrimaryDirpath = 'comment'
CommentClean1Dirpath = 'comment_clean1'
CommentClean2Dirpath = 'comment_clean2'
CommentClean3Dirpath = 'comment_clean3'


def clean_once(comment_primary_dirpath):
    files = os.listdir(comment_primary_dirpath)


