# -*- coding: utf-8 -*-
from model import loadSession, Distributor, Order, Discount, Product
import hashlib
from validator import REG_NICK, REG_SHA1, REG_EMAIL, checkParam
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from json_generator import json_error, json_login, json_logout, json_signup, json_neworder, json_products, json_pending_orders
from json_generator import json_ready_orders
from datetime import datetime
import json
import M2Crypto

class DAO:
    def __init__(self):
        self.session = loadSession()

    def expire_session(self):
        self.session.expire_all()

    def _get_random_hash (self):
        random_hash = hashlib.sha1(M2Crypto.m2.rand_bytes(2048)).hexdigest()
        return random_hash

    def login(self, email, password):
        if not checkParam(email, 50, REG_EMAIL):
            return ""

        try:
            distributor = self.session.query(Distributor).filter(Distributor.email == email).one()
        except NoResultFound:
            return json_error("UserOrPasswordIncorrect")
        hashed_pass = hashlib.sha1(password).hexdigest()
        if hashed_pass == distributor.password:
            if not distributor.session_id:
                session_id = self._get_random_hash()
                distributor.session_id = session_id
                try:
                    self.session.commit()
                except:
                    self.session.rollback()
                    return ""
            return json_login(distributor.session_id)
        else:
            return ""

    def logout(self, session_id):
        if not (checkParam(session_id, 40, REG_SHA1)):
            return json_error("InvalidParameter")

        distributor = self._get_distributor(session_id)
        if not distributor:
            return json_error("LogoutError")

        if distributor.session_id == session_id:
            distributor.session_id = ""
            try:
                self.session.commit()
            except:
                self.session.rollback()
                return json_error("Rollback")
            return json_logout()
        return json_error("LogoutError")

    def signup(self, name, email, password, telephone):
        if not (checkParam (name, 50, REG_NICK)
                and checkParam (email, 255, REG_EMAIL)):
            return json_error("InvalidParameter")

        hashed_pass = hashlib.sha1(password).hexdigest()

        new_distributor = Distributor(name=name, password=hashed_pass, email=email, telephone=telephone, session_id="")

        self.session.add(new_distributor)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return json_error("ExistingUserOrEmail")
        except:
            return json_error("Rollback")

        return json_signup()

    def neworder(self, session_id, json_order):
        distributor = self._get_distributor(session_id)

        if not distributor:
            return json_error("NotLoggedIn")

        order_dict = json.loads(json_order)

        product_id = order_dict["product_id"]
        amount = order_dict["amount"]

        try:
            product = self.session.query(Product).filter(Product.product_id == product_id).one()
        except:
            return json_error("ProductNonExistant")

        order = Order(datetime.utcnow(), amount)
        order.distributor_id = distributor.dist_id
        order.product_id = product.product_id
        self.session.add(order)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            return json_error("ProductNotAdded")

        #product_order = Product_Order(product_id=product.product_id, order_id=order.order_id)

        #self.session.add(product_order)

        #try:
            #self.session.commit()
        #except:
            #self.session.rollback()
            #return json_error("ProductNotAdded")

        return json_neworder(order.order_id)

    def list_products(self, session_id):
        distributor = self._get_distributor(session_id)

        if not distributor:
            return json_error("NotLoggedIn")

        try:
            products = self.session.query(Product).all()
        except:
            return json_error("error")

        products_dict = { "products" : [] }

        for p in products:
            products_dict["products"].append(
                { "product_id" : p.product_id,
                  "name" : p.name,
                  "description" : p.description,
                  "price" : p.price
                })

        return json_products(products_dict)

    def pending_orders(self, session_id):
        distributor = self._get_distributor(session_id)

        if not distributor:
            return json_error("NotLoggedIn")

        try:
            pending_orders = self.session.query(Order).join(Order.distributor).filter(Order.date_ready == None).all()
        except:
            return json_error("PendingOrdersError")

        return json_pending_orders(pending_orders)

    def ready_orders(self, session_id, since):
        distributor = self._get_distributor(session_id)

        since_datetime = datetime.fromtimestamp(int(since)//1000)

        if not distributor:
            return json_error("NotLoggedIn")

        try:
            ready_orders = self.session.query(Order).join(Order.distributor).filter(Order.date_ready > since_datetime).all()
        except:
            return json_error("ReadyOrdersError")

        return json_ready_orders(ready_orders)

    def orders(self, session_id):
        distributor = self._get_distributor(session_id)

        if not distributor:
            return json_error("NotLoggedIn")

        try:
            orders = self.session.query(Order).join(Order.distributor).all()
        except:
            return json_error("ReadyOrdersError")

        return json_



    #def get_stories(self, session_id, searchterm, page):
        ## TODO check rest of parameters
        #if not (checkParam (session_id, 40, REG_SHA1)):
            #return json_error("InvalidParameter")

        #page = int(page)

        #searchterm = "%" + searchterm + "%"
        #user_data = self._is_logged_in(session_id)
        #if not user_data:
            #return json_error("NotLoggedIn")
        #user_id, nick = user_data
        #try:
            #stories = self.session.query(Story).filter( Story.city.like(searchterm)
                                                       #| Story.languages.any(Story_Language.title.ilike(searchterm))
                                                       #| Story.languages.any(Story_Language.description.ilike(searchterm))
                                                      #).offset(page * 10).limit(10).all()
        #except NoResultFound:
            #return json_error("NoResults")

        #stories = self._add_avg_rating(stories)

        #return json_stories(stories, nick)

    #def get_stories_by_city(self, session_id, city, page):
        ## TODO check rest of parameters
        #if not (checkParam (session_id, 40, REG_SHA1)):
            #return json_error("InvalidParameter")

        #page = int(page)

        #user_data = self._is_logged_in(session_id)
        #if not user_data:
            #return json_error("NotLoggedIn")
        #user_id, nick = user_data
        #try:
            #stories = self.session.query(Story).filter(Story.city.ilike("%" + city + "%")).offset(page * 10).limit(10).all()
        #except NoResultFound:
            #return json_error("NoResults")

        #stories = self._add_avg_rating(stories)

        #return json_stories(stories, nick)

    ## Language?
    #def get_story(self, session_id, story_id):
        #if not (checkParam (session_id, 40, REG_SHA1)):
            #return json_error("InvalidParameter")

        #try:
            #story = self.session.query(Story).filter(Story.storyId == story_id).one()
        #except NoResultFound:
            #return json_error("StoryNonExistant")

        ## Just the first language for now
        #text_json = story.languages[0].text_json
        #image_json = story.image_json

        #user_data = self._is_logged_in(session_id)

        #if not user_data:
            #return json_error("UserNotLoggedIn")

        #user_id, nick = user_data

        #try:
            #user_story = self.session.query(User_Story).filter((User_Story.userId
                                                              #== user_id) &
                                                              #(User_Story.storyId
                                                              #== story_id)).one()
        #except NoResultFound:
            #user_story = User_Story(userId=user_id, storyId=story_id)
            #self.session.add(user_story)

            #self.session.commit()
        #except:
            #self.session.rollback()
            #return json_error("Rollback")


        #return json_story(text_json, image_json)

    #def get_stories_by_user(self, session_id, page):
        #if not (checkParam (session_id, 40, REG_SHA1)):
            #return json_error("InvalidParameter")

        #page = int(page)

        #user_data = self._is_logged_in(session_id)
        #if not user_data:
            #return json_error("NotLoggedIn")
        #user_id, nick = user_data
        #try:
            #user_stories = self.session.query(User_Story).filter(User_Story.userId == user_id).all()
            #stories = [us.story for us in user_stories]
        #except NoResultFound:
            #return json_error("NoResults")

        #stories = self._add_avg_rating(stories)

        #return json_stories(stories, nick)

    ## Verification? language?
    #def add_story(self, title, description, price, image, city, json_text, json_images, languageId=1,
                  #creator=1):
        #story = Story(price=int(price), city=city, image=image, creatorId=creator)

        #self.session.add(story)
        #try:
            #self.session.commit()
        #except:
            #self.session.rollback()
            #return json_error("Rollback")

        #json_text = create_json_text(json_text)
        #json_images = create_json_images(json_images)

        ## FIXME hardcoded language
        #filename_text = str(story.storyId) + "_text_" + "es.json"
        #filename_images = str(story.storyId) + "_images.json"

        #text_path = save_json(json_text, filename_text)
        #images_path = save_json(json_images, filename_images)

        #story.image_json = images_path

        #story_language = Story_Language(storyId=story.storyId, languageId=languageId,
                                        #title=title, description=description,
                                        #text_json=text_path)

        #self.session.add(story_language)

        #try:
            #self.session.commit()
        #except:
            #self.session.rollback()
            #return json_error("Rollback")

        #return None

    #def validate(self, validation_hash):
        #user = self._get_user(validation_hash)

        #if user:
            #user.Validated = True
        #else:
            #return json_error("ValidationError")

        #try:
            #self.session.commit()
        #except:
            #self.session.rollback()
            #return json_error("ValidationError")

        #self.logout(validation_hash, user.nick)

        #return html_confirmation()

    #def _send_validation(self, user):
        #validation_hash = self._get_random_hash()
        #subject = "Valídate en Turiskana!"
        #text = "Hola, entra en este link para completar tu registro: " + \
               #"http://api.turiskana.com/validate/" + validation_hash

        #user.session_id = validation_hash

        #try:
            #self.session.commit()
        #except:
            #self.session.rollback()
            #return False

        #return send_email(user.email, subject, text)

    def _get_distributor(self, session_id):
        try:
            distributor = self.session.query(Distributor).filter(Distributor.session_id == session_id).one()
            return distributor
        except:
            return None

    def _is_logged_in(self, session_id):
        try:
            distributor = self.session.query(Distributor).filter(Distributor.session_id == session_id).one()
            if distributor.Validated == False:
                return None
            return distributor.distributor_id, distributor.email
        except NoResultFound:
            return None

