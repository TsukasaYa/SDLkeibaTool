#---戦績のフィルタを行うクラス
class FormFilter:

  def __init__(self, pre=None, post=None, smile=None, course=None, style=None, race=None):
    self.pre = pre
    self.post = post
    self.smile = smile
    self.course = course
    self.style = style
    self.race = race
  
  def filter(self, form):
    rslt = form
    if self.pre is not None:
      rslt = self.get_n_form(rslt, self.pre)
    if self.smile is not None:
      rslt = self.get_form_by_smile(rslt, self.smile)
    if self.course is not None:
      rslt = self.get_form_by_course(rslt, self.course)
    if self.style is not None:
      rslt = self.get_form_by_style(rslt, self.style)
    if self.race is not None:
      rslt = self.get_form_by_race(rslt, self.race)
    if self.post is not None:
      rslt = self.get_n_form(rslt, self.post)
    return rslt

    #arr:SMILE区分、 subset of ['S','M','I','L','E']
    def get_form_by_smile(self, form, smile):
    return form.query('SMILE in @smile')

    #指定されたコースの戦績を抽出 course : string[]
    def get_form_by_course(self, form, course):
    filter_list = [c[1:3] in course for c in form['開催']]
    return form[filter_list]

    #指定された脚質で走っていた戦績を抽出 style = subset of ['逃','先','差','追','マ']
    def get_form_by_style(self, form, style):
    return form.query('style in @style')

    #該当するレース名で抽出
    def get_form_by_race(self, form, race):
    race = race.replace('(','\(').replace(')','\)')
    return form.query('レース名.str.contains(@race)')

    #前n走
    def get_n_form(self, form, n):
    n = max(len(form),n)
    return form[0:n]