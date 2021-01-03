from django.db import models

class Subreddit(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    description_html = models.CharField(max_length=5000)
    subscribers = models.IntegerField(default=0)
    created_utc = models.DateTimeField()
    def __str__(self):
        return self.title

#region pprint subreddit
# {
#BAD=> 'accounts_active': 39,
#BAD=> 'accounts_active_is_fuzzed': False,
#BAD=> 'active_user_count': 39,
#BAD=> 'advertiser_category': '',
#BAD=> 'all_original_content': False,
#BAD=> 'allow_discovery': True,
#BAD=> 'allow_galleries': True,
#BAD=> 'allow_images': True,
#BAD=> 'allow_polls': True,
#BAD=> 'allow_predictions': False,
#BAD=> 'allow_videogifs': True,
#BAD=> 'allow_videos': True,
#BAD=> 'banner_background_color': '',
#BAD=> 'banner_background_image': '',
#BAD=> 'banner_img': '',
#BAD=> 'banner_size': None,
#BAD=> 'can_assign_link_flair': False,
#BAD=> 'can_assign_user_flair': False,
#BAD=> 'collapse_deleted_comments': False,
#BAD=> 'comment_score_hide_mins': 0,
#BAD=> 'community_icon': '',
#BAD=> 'created': 1581462904.0,
#BAD=> 'created_utc': 1581434104.0,
#GOOD=> 'description': 'COVID2019',
#GOOD=> 'description_html': '<!-- SC_OFF --><div class="md"><p>COVID2019</p>\n''</div><!-- SC_ON -->',
#BAD=> 'disable_contributor_requests': False,
#GOOD=> 'display_name': 'COVID',
#GOOD=> 'display_name_prefixed': 'r/COVID',
#BAD=> 'emojis_custom_size': None,
#BAD=> 'emojis_enabled': False,
#BAD=> 'free_form_reports': True,
#BAD=> 'has_menu_widget': False,
#BAD=> 'header_img': None,
#BAD=> 'header_size': None,
#BAD=> 'header_title': '',
#BAD=> 'hide_ads': False,
#BAD=> 'icon_img': '',
#BAD=> 'icon_size': None,
#BAD=> 'id': '2f4kx6',
#BAD=> 'is_crosspostable_subreddit': False,
#BAD=> 'is_enrolled_in_new_modmail': None,
#BAD=> 'key_color': '',
#GOOD=> 'lang': 'en',
#BAD=> 'link_flair_enabled': False,
#BAD=> 'link_flair_position': '',
#BAD=> 'mobile_banner_image': '',
#GOOD=> 'name': 't5_2f4kx6',
#BAD=> 'notification_level': None,
#BAD=> 'original_content_tag_enabled': False,
#BAD=> 'over18': False,
#BAD=> 'primary_color': '',
#GOOD=> 'public_description': 'COVID-19 News, Etc.',
#GOOD=> 'public_description_html': '<!-- SC_OFF --><div class="md"><p>COVID-19 News, '
# 'public_traffic': False,
# 'quarantine': False,
# 'restrict_commenting': False,
# 'restrict_posting': True,
#BAD=> 'show_media': True,
#BAD=> 'show_media_preview': True,
#BAD=> 'spoilers_enabled': True,
#BAD=> 'submission_type': 'any',
#BAD=> 'submit_link_label': '',
#BAD=> 'submit_text': '',
#BAD=> 'submit_text_html': None,
#BAD=> 'submit_text_label': '',
#GOOD=> 'subreddit_type': 'public',
#GOOD=> 'subscribers': 7677,
#BAD=> 'suggested_comment_sort': None,
#GOOD=> 'title': 'Novel Coronavirus News, Analysis, Survival Stories, Etc.',
#GOOD=> 'url': '/r/COVID/',
#BAD=> 'user_can_flair_in_sr': None,
#BAD=> 'user_flair_background_color': None,
#BAD=> 'user_flair_css_class': None,
#BAD=> 'user_flair_enabled_in_sr': True,
#BAD=> 'user_flair_position': 'right',
#BAD=> 'user_flair_richtext': [],
#BAD=> 'user_flair_template_id': None,
#BAD=> 'user_flair_text': None,
#BAD=> 'user_flair_text_color': None,
#BAD=> 'user_flair_type': 'text',
#BAD=> 'user_has_favorited': None,
#BAD=> 'user_is_banned': None,
#BAD=> 'user_is_contributor': None,
#BAD=> 'user_is_moderator': None,
#BAD=> 'user_is_muted': None,
#BAD=> 'user_is_subscriber': None,
#BAD=> 'user_sr_flair_enabled': None,
#BAD=> 'user_sr_theme_enabled': True,
#BAD=> 'videostream_links_count': 1,
#BAD=> 'whitelist_status': 'all_ads',
#BAD=> 'wiki_enabled': False,
#BAD=> 'wls': 6}
#endregion

class AuthorRedditor(models.Model):
    id = models.AutoField(primary_key=True)
    redditor_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    created_utc = models.DateTimeField()

    def __str__(self):
        return self.title

#region autor pprint
# {
#GOOD=> 'awardee_karma': 0,
#GOOD=> 'awarder_karma': 0,
#GOOD=> 'comment_karma': 343,
#GOOD=> 'created': 1400644705.0,
#GOOD=> 'created_utc': 1400615905.0,
#BAD=> 'has_subscribed': True,
#BAD=> 'has_verified_email': True,
#BAD=> 'hide_from_robots': False,
#BAD=> 'icon_img': 'https://www.redditstatic.com/avatars/avatar_default_01_24A0ED.png',
#GOOD=>  'id': 'gnc18',
#BAD=> 'is_employee': False,
#BAD=> 'is_friend': False,
#BAD=> 'is_gold': False,
#BAD=> 'is_mod': False,
#GOOD=>  'link_karma': 506,
#GOOD=>  'name': 'GD3123',
#BAD=> 'pref_show_snoovatar': False,
#BAD=> 'snoovatar_img': '',
#BAD=> 'snoovatar_size': None,
#BAD=> 'subreddit': {'banner_img': '',
#               'banner_size': None,
#               'community_icon': None,
#               'default_set': True,
#               'description': '',
#               'disable_contributor_requests': False,
#               'display_name': 'u_GD3123',
#               'display_name_prefixed': 'u/GD3123',
#               'free_form_reports': True,
#               'header_img': None,
#               'header_size': None,
#               'icon_color': '#24A0ED',
#               'icon_img': 'https://www.redditstatic.com/avatars/avatar_default_01_24A0ED.png',
#               'icon_size': [256, 256],
#               'is_default_banner': True,
#               'is_default_icon': True,
#               'key_color': '',
#               'link_flair_enabled': False,
#               'link_flair_position': '',
#               'name': 't5_1qom7t',
#               'over_18': False,
#               'previous_names': [],
#               'primary_color': '',
#               'public_description': '',
#               'quarantine': False,
#               'restrict_commenting': False,
#               'restrict_posting': True,
#               'show_media': True,
#               'submit_link_label': '',
#               'submit_text_label': '',
#               'subreddit_type': 'user',
#               'subscribers': 0,
#               'title': '',
#               'url': '/user/GD3123/',
#               'user_is_banned': None,
#               'user_is_contributor': None,
#               'user_is_moderator': None,
#               'user_is_muted': None,
#               'user_is_subscriber': None},
#GOOD=> 'total_karma': 849,
#GOOD=> 'verified': True}
#endregion
class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.CharField(max_length=50, unique=True)
    redditor = models.ForeignKey(AuthorRedditor, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    selftext =  models.CharField(max_length=5000)
    link_flair_template_id = models.CharField(max_length=500, null=True)
    link_flair_text = models.CharField(max_length=500, null=True)
    num_comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    upvote_ratio = models.FloatField(default=0.0)
    created_utc = models.DateTimeField()

    def __str__(self):
        return self.title

#region pprint submisson
#  {
#BAD=> 'all_awardings': [],
#BAD=> 'allow_live_comments': False,
#BAD=> 'approved_at_utc': None,
#BAD=> 'approved_by': None,
#GOOD=> 'archived': True,
#GOOD=> 'author': Redditor(name='blackwingbear'),
#BAD=> 'author_flair_background_color': None,
#BAD=> 'author_flair_css_class': None,
#BAD=> 'author_flair_richtext': [],
#BAD=> 'author_flair_template_id': None,
#BAD=> 'author_flair_text': None,
#BAD=> 'author_flair_text_color': None,
#BAD=> 'author_flair_type': 'text',
#BAD=> 'author_fullname': 't2_90nmy',
#BAD=> 'author_patreon_flair': False,
#BAD=> 'author_premium': False,
#BAD=> 'awarders': [],
#BAD=> 'banned_at_utc': None,
#BAD=> 'banned_by': None,
#BAD=> 'can_gild': False,
#BAD=> 'can_mod_post': False,
#GOOD=> 'category': None,
#BAD=> 'clicked': False,
#GOOD=> 'comment_limit': 2048,
#GOOD=> 'comment_sort': 'confidence',
#BAD=> 'content_categories': None,
#BAD=> 'contest_mode': False,
#GOOD=> 'created': 1589952542.0,
#GOOD=> 'created_utc': 1589923742.0,
#BAD=> 'discussion_type': None,
#BAD=> 'distinguished': None,
#BAD=> 'domain': 'self.COVID',
#GOOD=> 'downs': 0,
#BAD=> 'edited': False,
#GOOD=> 'gilded': 0,
#GOOD=> 'gildings': {},
#BAD=> 'hidden': False,
#BAD=> 'hide_score': False,
#GOOD=> 'id': 'gmxq55',
#BAD=> 'is_crosspostable': False,
#BAD=> 'is_meta': False,
#BAD=> 'is_original_content': False,
#BAD=> 'is_reddit_media_domain': False,
#BAD=> 'is_robot_indexable': True,
#BAD=> 'is_self': True,
#BAD=> 'is_video': False,
#BAD=> 'likes': None,
#BAD=> 'link_flair_background_color': '',
#BAD=> 'link_flair_css_class': None,
#BAD=> 'link_flair_richtext': [],
#GOOD=> 'link_flair_text': None,
#BAD=> 'link_flair_text_color': 'dark',
#BAD=> 'link_flair_type': 'text',
#BAD=> 'locked': False,
#BAD=> 'media': None,
#BAD=> 'media_embed': {},
#BAD=> 'media_only': False,
#BAD=> 'mod_note': None,
#BAD=> 'mod_reason_by': None,
#BAD=> 'mod_reason_title': None,
#BAD=> 'mod_reports': [],
#GOOD=> 'name': 't3_gmxq55',
#BAD=> 'no_follow': True,
#GOOD=> 'num_comments': 5,
#BAD=> 'num_crossposts': 0,
#BAD=> 'num_reports': None,
#BAD=> 'over_18': False,
#BAD=> 'parent_whitelist_status': 'all_ads',
#GOOD=> 'permalink': '/r/COVID/comments/gmxq55/the_united_states_has_over_90000_cases_of_covid19/',
#BAD=> 'pinned': False,
#BAD=> 'pwls': 6,
#BAD=> 'quarantine': False,
#BAD=> 'removal_reason': None,
#BAD=> 'removed_by': None,
#BAD=> 'removed_by_category': None,
#BAD=> 'report_reasons': None,
#BAD=> 'saved': False,
#GOOD=> 'score': 1,
#BAD=> 'secure_media': None,
#BAD=> 'secure_media_embed': {},
#GOOD=> 'selftext': '',
#GOOD=> 'selftext_html': None,
#BAD=> 'send_replies': True,
#BAD=> 'spoiler': False,
#BAD=> 'stickied': False,
#GOOD=> 'subreddit': Subreddit(display_name='COVID'),
#BAD=> 'subreddit_id': 't5_2f4kx6',
#BAD=> 'subreddit_name_prefixed': 'r/COVID',
#BAD=> 'subreddit_subscribers': 7677,
#BAD=> 'subreddit_type': 'public',
#BAD=> 'suggested_sort': None,
#BAD=> 'thumbnail': 'self',
#BAD=> 'thumbnail_height': None,
#BAD=> 'thumbnail_width': None,
#GOOD=> 'title': 'The United States has over 90,000 cases of CoViD-19. Of those, '
#          'Georgia has over 38,000.. Over 1/3 out of the total. The "You '
#          'can\'t tell me what to do! I\'m a rebel!" state is WINNING.',
#BAD=> 'top_awarded_type': None,
#BAD=> 'total_awards_received': 0,
#BAD=> 'treatment_tags': [],
#GOOD=> 'ups': 1,
#GOOD=> 'upvote_ratio': 0.52,
#GOOD=> 'url': 'https://www.reddit.com/r/COVID/comments/gmxq55/the_united_states_has_over_90000_cases_of_covid19/',
#BAD=> 'user_reports': [],
#BAD=> 'view_count': None,
#BAD=> 'visited': False,
#BAD=> 'whitelist_status': 'all_ads',
#BAD=> 'wls': 6}
#endregion

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.CharField(max_length=50, unique=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    redditor = models.ForeignKey(AuthorRedditor, on_delete=models.CASCADE)
    parent_id = models.CharField(max_length=50)
    body = models.CharField(max_length=5000)
    body_html = models.CharField(max_length=5000)
    is_submitter = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    created_utc = models.DateTimeField()

    def __str__(self):
        return self.title
 
#region pprint comments
#BAD=> 'all_awardings': [],
#BAD=> 'approved_at_utc': None,
#BAD=> 'approved_by': None,
#BAD=> 'archived': True,
#BAD=> 'associated_award': None,
#GOOD=> 'author': Redditor(name='ProtiK'),
#BAD=> 'author_flair_background_color': None,
#BAD=> 'author_flair_css_class': None,
#BAD=> 'author_flair_richtext': [],
#BAD=> 'author_flair_template_id': None,
#BAD=> 'author_flair_text': None,
#BAD=> 'author_flair_text_color': None,
#BAD=> 'author_flair_type': 'text',
#BAD=> 'author_fullname': 't2_51ou4',
#BAD=> 'author_patreon_flair': False,
#BAD=> 'author_premium': False,
#BAD=> 'awarders': [],
#BAD=> 'banned_at_utc': None,
#BAD=> 'banned_by': None,
#GOOD=> 'body': "That's correct. The exact process is very location-dependent but "
#         'follows the same general form wherever you go (in the US). Tenant is '
#         'given a notice of noncompliance, to which they then have a certain '
#         'amount of time to respond. Rinse and repeat this process 2-3 times. '
#         'The tenant then is given an eviction notice, which has a specific '
#         'response window as well. After the eviction period has ended, the '
#         'landlord can then (and only then) contact the jurisdictional law '
#         'enforcement agency and appeal for forcible removal. \n'
#         '\n'
#         'As you mentioned, there are several points throughout the process '
#         'where a knowledgeable tenant can drag out the process. In any case, '
#         "OP can't possibly be at the last step of the eviction process "
#         'without knowing he has a rightful eviction staring him in the face. '
#         "OP wouldn't just maybe have a case; he would have a rock-solid case "
#         'against the HOA for wrongful eviction.\n'
#         '\n'
#         "Even if the HOA's CC&Rs have hoops to jump through for a homeowner "
#         'to lease their home legally, OP is still a tenant of the building. '
#         'There is no "false construction" of tenancy - you\'re a tenant, or '
#         "you're not. Because he is legally a tenant, he is afforded all legal "
#         'rights that come with it, due process in eviction included.',
#GOOD=> 'body_html': '<div class="md"><p>That&#39;s correct. The exact process is '
#              'very location-dependent but follows the same general form '
#              'wherever you go (in the US). Tenant is given a notice of '
#              'noncompliance, to which they then have a certain amount of time '
#              'to respond. Rinse and repeat this process 2-3 times. The tenant '
#              'then is given an eviction notice, which has a specific response '
#              'window as well. After the eviction period has ended, the '
#              'landlord can then (and only then) contact the jurisdictional '
#              'law enforcement agency and appeal for forcible removal. </p>\n'
#              '\n'
#              '<p>As you mentioned, there are several points throughout the '
#              'process where a knowledgeable tenant can drag out the process. '
#              'In any case, OP can&#39;t possibly be at the last step of the '
#              'eviction process without knowing he has a rightful eviction '
#              'staring him in the face. OP wouldn&#39;t just maybe have a '
#              'case; he would have a rock-solid case against the HOA for '
#              'wrongful eviction.</p>\n'
#              '\n'
#              '<p>Even if the HOA&#39;s CC&amp;Rs have hoops to jump through '
#              'for a homeowner to lease their home legally, OP is still a '
#              'tenant of the building. There is no &quot;false '
#              'construction&quot; of tenancy - you&#39;re a tenant, or '
#              'you&#39;re not. Because he is legally a tenant, he is afforded '
#              'all legal rights that come with it, due process in eviction '
#              'included.</p>\n'
#              '</div>',
#BAD=> 'can_gild': True,
#BAD=> 'can_mod_post': False,
#BAD=> 'collapsed': False,
#BAD=> 'collapsed_because_crowd_control': None,
#BAD=> 'collapsed_reason': None,
#GOOD=> 'comment_type': None,
#GOOD=> 'controversiality': 0,
#GOOD=> 'created': 1586477434.0,
#GOOD=> 'created_utc': 1586448634.0,
#GOOD=> 'depth': 5,
#BAD=> 'distinguished': None,
#GOOD=> 'downs': 0,
#BAD=> 'edited': 1586448998.0,
#GOOD=> 'gilded': 0,
#BAD=> 'gildings': {},
#GOOD=> 'id': 'fmwlc2w',
#BAD=> 'is_submitter': False,
#BAD=> 'likes': None,
#GOOD=> 'link_id': 't3_fwtkgz',
#BAD=> 'locked': False,
#BAD=> 'mod_note': None,
#BAD=> 'mod_reason_by': None,
#BAD=> 'mod_reason_title': None,
#BAD=> 'mod_reports': [],
#GOOD=> 'name': 't1_fmwlc2w',
#BAD=> 'no_follow': True,
#BAD=> 'num_reports': None,
#GOOD=> 'parent_id': 't1_fmwjdd5',
#GOOD=> 'permalink': '/r/COVID/comments/fwtkgz/being_illegally_kicked_out_of_my_residence_during/fmwlc2w/',
#BAD=> 'removal_reason': None,
#BAD=> 'report_reasons': None,
#BAD=> 'saved': False,
#GOOD=> 'score': 1,
#BAD=> 'score_hidden': False,
#BAD=> 'send_replies': True,
#BAD=> 'stickied': False,
#GOOD=> 'subreddit': Subreddit(display_name='COVID'),
#BAD=> 'subreddit_id': 't5_2f4kx6',
#BAD=> 'subreddit_name_prefixed': 'r/COVID',
#BAD=> 'subreddit_type': 'public',
#BAD=> 'top_awarded_type': None,
#BAD=> 'total_awards_received': 0,
#BAD=> 'treatment_tags': [],
#GOOD=> 'ups': 1,
#BAD=> 'user_reports': []}
#endregion
