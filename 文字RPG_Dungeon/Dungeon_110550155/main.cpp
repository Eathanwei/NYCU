#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

void Gamestart();
void Gamerestart();
void Gameloadstart();
void Gamesavedata();
bool gameover;

class Object
{
private:
    string name,script;
    bool exist;
public:
    Object();
    Object(string n, string s):name(n), script(s), exist(1){}

    /* pure virtual function */
    virtual bool triggerEvent(){
        return 0;
    }

    /* Set & Get function*/
    void setName(string n){
        name=n;
    }
    string getName(){
        return name;
    }
    void setScript(string n){
        script=n;
    }
    void setExist(bool x){
        exist=x;
    }
    string getScript(){
        return script;
    }
    bool getExist(){
        return exist;
    }
};

class Room
{
private:
    Room* upRoom;
    Room* downRoom;
    Room* leftRoom;
    Room* rightRoom;
    Object* object1;
    Object* object2;
    int index1;
    int index2;
    bool object1exist,object2exist;
    bool allowup,allowdown,allowleft,allowright;
public:
    Room(int x1, int x2, bool y1, bool y2, bool y3, bool y4):index1(x1), index2(x2), object1exist(0), object2exist(0), allowup(y1), allowdown(y2), allowleft(y3), allowright(y4){}

    /* Set & Get function*/
    void setUpRoom(Room* x){
        upRoom=x;
    }
    void setDownRoom(Room* x){
        downRoom=x;
    }
    void setLeftRoom(Room* x){
        leftRoom=x;
    }
    void setRightRoom(Room* x){
        rightRoom=x;
    }
    void setObject1(Object* x){
        object1=x;
        object1exist=1;
    }
    void setObject2(Object* x){
        object2=x;
        object2exist=1;
    }
    void setIndex1(int x){
        index1=x;
    }
    void setIndex2(int x){
        index2=x;
    }
    void allow(bool x1, bool x2, bool x3, bool x4){
        allowup=x1;
        allowdown=x2;
        allowleft=x3;
        allowright=x4;
    }
    Room* getUpRoom(){
        return upRoom;
    }
    Room* getDownRoom(){
        return downRoom;
    }
    Room* getLeftRoom(){
        return leftRoom;
    }
    Room* getRightRoom(){
        return rightRoom;
    }
    Object* getObject1(){
        return object1;
    }
    Object* getObject2(){
        return object2;
    }
    int getIndex1(){
        return index1;
    }
    int getIndex2(){
        return index2;
    }
    bool getobject1exist(){
        return object1exist;
    }
    bool getobject2exist(){
        return object2exist;
    }
    bool getallowup(){
        return allowup;
    }
    bool getallowdown(){
        return allowdown;
    }
    bool getallowleft(){
        return allowleft;
    }
    bool getallowright(){
        return allowright;
    }
    void menu();
};

Room rooms[6][5]={
{Room(0,0,0,1,0,0),Room(0,1,1,0,0,0),Room(0,2,0,0,0,1),Room(0,3,1,1,1,0),Room(0,4,1,1,1,1)},
{Room(1,0,0,1,0,0),Room(1,1,1,0,0,0),Room(1,2,0,0,1,1),Room(1,3,0,1,1,1),Room(1,4,0,0,1,0)},
{Room(2,0,0,1,0,0),Room(2,1,1,0,0,0),Room(2,2,0,0,1,1),Room(2,3,1,0,1,1),Room(2,4,0,0,1,0)},
{Room(3,0,0,1,0,0),Room(3,1,1,0,0,0),Room(3,2,0,1,1,1),Room(3,3,0,0,1,1),Room(3,4,0,0,1,0)},
{Room(4,0,0,1,0,0),Room(4,1,1,0,0,0),Room(4,2,1,0,1,1),Room(4,3,0,0,1,1),Room(4,4,0,0,1,0)},
{Room(5,0,0,1,0,0),Room(5,1,1,0,0,0),Room(5,2,1,1,0,0),Room(5,3,0,0,1,0),Room(5,4,1,1,1,1)}};

class GameCharacter: public Object
{
private:
    int maxHealth;
    int currentHealth;
    int attack;
    int defense;
    int type;
public:
    GameCharacter();
    GameCharacter(string n, string s,int x,int y,int z):Object(n, s), maxHealth(x), currentHealth(x), attack(y), defense(z){}
    /* Set & Get function*/
    void setMaxHealth(int x){
        maxHealth=x;
    }
    void setCurrentHealth(int x){
        currentHealth=x;
    }
    void setAttack(int x){
        attack=x;
    }
    void setDefense(int x){
        defense=x;
    }
    void setType(int x){
        type=x;
    }
    int getMaxHealth(){
        return maxHealth;
    }
    int getCurrentHealth(){
        return currentHealth;
    }
    int getAttack(){
        return attack;
    }
    int getDefense(){
        return defense;
    }
    int getType(){
        return type;
    }
    string getTypename(){
        if(type==0){
            return "water";
        }else if(type==1){
            return "fire";
        }else{
            return "grass";
        }
    }
};

class Player: public GameCharacter
{
private:
    int coin;
    Room* currentRoom;
public:
    Player();
    Player(string n, string s, int x,int y,int z):GameCharacter(n, s, x, y, z),coin(0){};
    /* Virtual function that you need to complete   */
    /* In Player, this function should show the     */
    /* status of player.                            */

    /* Set & Get function*/
    void setCurrentRoom(Room* x){
        currentRoom=x;
    }
    void setCoin(int x){
        coin=x;
    }
    Room* getCurrentRoom(){
        return currentRoom;
    }
    int getCoin(){
        return coin;
    }
};

Player play("name","",100,15,0);

class Monster: public GameCharacter
{
private:
    bool poisoned;
public:
    Monster():GameCharacter("Monster", "fight with the monster", 50, 25, 5),poisoned(0){}

    /* Virtual function that you need to complete   */
    /* In Monster, this function should deal with   */
    /* the combat system.                           */
    bool triggerEvent();
    void setpoisoned(bool x){
        poisoned=x;
    }
    bool getpoisoned(){
        return poisoned;
    }
    int typecounter(){
        if(getType()==play.getType()){
            return 0;
        }else if(getType()==0&&play.getType()==2){
            return 5;
        }else if(getType()-play.getType()==1){
            return 5;
        }else{
            return -5;
        }
    }
    void fight();
};

Monster monster1,monster2;

class Boss: public GameCharacter
{
private:
    bool poisoned;
public:
    Boss():GameCharacter("Boss", "fight with the boss", 100, 35, 10),poisoned(0){}

    /* Virtual function that you need to complete   */
    /* In Monster, this function should deal with   */
    /* the combat system.                           */
    bool triggerEvent();
    void setpoisoned(bool x){
        poisoned=x;
    }
    bool getpoisoned(){
        return poisoned;
    }
    int typecounter(){
        if(getType()==play.getType()){
            return 0;
        }else if(getType()==0&&play.getType()==2){
            return 5;
        }else if(getType()-play.getType()==1){
            return 5;
        }else{
            return -5;
        }
    }
    void fight();
};

Boss boss;

class Coin: public Object
{
private:
public:
    Coin():Object("coin", "open the chest"){}
    bool triggerEvent(){
        play.setCoin(play.getCoin()+100);
        setExist(0);
        cout << endl << "You get 100 coins." << endl;
    }
};

Coin coins1,coins2,coins3;

class Gem: public Object
{
private:
public:
    Gem():Object("magic gem", "open the chest"){}
    bool triggerEvent(){
        setExist(0);
        cout << endl << "You get a gem. You can use it to change your type with witch's help." << endl;
    }
};

Gem gem;

class Key: public Object
{
private:
public:
    Key():Object("key", "open the chest"){}
    bool triggerEvent(){
        setExist(0);
        cout << endl << "You get a key. You can unlock the door." << endl;
    }
};

Key key;

class Lock: public Object
{
private:
public:
    Lock():Object("lock", "unlock the door"){}
    bool triggerEvent(){
        if(key.getExist()==0){
            setExist(0);
            rooms[5][2].allow(1,1,0,1);
            cout << endl << "You open the door." << endl;
        }else{
            cout << endl << "You don't have a key." << endl;
        }
    }
};

Lock lock;

class Poison: public Object
{
private:
    bool used;
public:
    Poison():Object("poison", "pick up the poison"),used(0){}
    void setUsed(bool x){
        used=x;
    }
    bool getUsed(){
        return used;
    }
    bool triggerEvent(){
        setExist(0);
        cout << endl << "You get the poison. It can do 10 damage to monster or boss every turn." << endl;
    }
};

Poison poison;

class Potion: public Object
{
private:
    bool used;
public:
    Potion():Object("potion", "pick up the potion"),used(0){}
    void setUsed(bool x){
        used=x;
    }
    bool getUsed(){
        return used;
    }
    bool triggerEvent(){
        setExist(0);
        cout << endl << "You get the potion. It can recover 20 health." << endl;
    }
    void use(){
        used=1;
        if(play.getMaxHealth()-play.getCurrentHealth()<20){
            play.setCurrentHealth(play.getMaxHealth());
        }else{
            play.setCurrentHealth(play.getCurrentHealth()+20);
        }
        cout << endl << "You use the potion. Your health is " << play.getCurrentHealth() << "/" << play.getMaxHealth() << " now." << endl;
    }
};

Potion potions[2];

class Item: public Object
{
private:
    int health,attack,defense;
    Item* samepart1;
    Item* samepart2;
    bool disappear;
    bool wore;
public:
    Item();
    Item(string n, string s, int x, int y, int z):Object(n, s), health(x), attack(y), defense(z), disappear(0), wore(0){}

    /* Virtual function that you need to complete    */
    /* In Item, this function should deal with the   */
    /* pick up action. You should add status to the  */
    /* player.                                       */
    bool triggerEvent(){
        setExist(0);
        cout << endl << "You get the " << getName() << "." << endl;
    };

    /* Set & Get function*/
    int getHealth(){
        return health;
    }
    int getAttack(){
        return attack;
    }
    int getDefense(){
        return defense;
    }
    bool getWore(){
        return wore;
    }
    bool getDisappear(){
        return disappear;
    }
    void setDisappear(bool x){
        disappear=x;
    }
    void setWore(bool x){
        wore=x;
    }
    void setsamepart1(Item* x){
        samepart1=x;
    }
    void setsamepart2(Item* x){
        samepart2=x;
    }
    void takeoffnomenu(){
        wore=0;
        cout << "You take off the " << getName() << "." << endl;
        play.setAttack(play.getAttack()-attack);
        play.setCurrentHealth(play.getCurrentHealth()-health);
        play.setDefense(play.getDefense()-defense);
        play.setMaxHealth(play.getMaxHealth()-health);
        if(play.getCurrentHealth()<=0){
            return;
        }
    }
    void takeoff(){
        wore=0;
        cout << "You take off the " << getName() << "." << endl;
        play.setAttack(play.getAttack()-attack);
        play.setCurrentHealth(play.getCurrentHealth()-health);
        play.setDefense(play.getDefense()-defense);
        play.setMaxHealth(play.getMaxHealth()-health);
        if(play.getCurrentHealth()<=0){
            return;
        }
    }
    void wear(){
        if(samepart1->wore){
            samepart1->takeoffnomenu();
        }
        if(samepart2->wore){
            samepart2->takeoffnomenu();
        }
        wore=1;
        cout << "You put on the " << getName() << "." << endl;
        play.setAttack(play.getAttack()+attack);
        play.setCurrentHealth(play.getCurrentHealth()+health);
        play.setDefense(play.getDefense()+defense);
        play.setMaxHealth(play.getMaxHealth()+health);
    }
};

Item items[9]={Item("helmet", "pick up the helmet", 0, 0, 5), Item("armor", "pick up the armor", 0, 0, 5), Item("shield", "pick up the shield", 0, 0, 5),
Item("bulletproof shield", "", 0, 0, 10), Item("robe", "", 10, 0, 10), Item("sword", "pick up the sword", 0, 20, 0),
Item("poison sword", "", 0, 25, 0), Item("wand", "", 0, 15, 0), Item("spell book", "", 0, 10, 0)};

class Girl: public Object
{
private:
public:
    Girl():Object("girl", "talk to the girl"){}
    bool triggerEvent(){
        string s;
        cout << endl << "Girl : Can you buy these matches with 50 coin?" << endl << "A. ignore her" << endl << "B. buy the matches"
        << endl << "C. kill her" << endl << "D. go back to menu" << endl;
        cin >> s;
        if(s=="A"){
            setExist(0);
            if(play.getCurrentRoom()->getIndex1()==3){
                monster2.setExist(1);
            }else{
                monster2.setExist(1);
            }
            cout << endl << "The girl become a monster." << endl;
        }else if(s=="B"){
            if(play.getCoin()<50){
                cout << endl << "You don't have 50 coins." << endl;
            }else{
                setExist(0);
                play.setCoin(play.getCoin()-50);
                cout << endl << "The girl leave." << endl;
                rooms[3][4].allow(1,1,1,1);
                rooms[4][4].allow(1,1,1,1);
            }
        }else if(s=="C"){
            setExist(0);
            if(play.getCurrentRoom()->getIndex1()==3){
                monster2.setExist(1);
            }else{
                monster2.setExist(1);
            }
            cout << endl << "The girl become a monster before you kill her." << endl;
        }else if(s=="D"){
        }else{
            cout << endl << "Error input!" << endl;
        }
    }
};

Girl girl;

class Witch: public Object
{
private:
public:
    Witch():Object("witch", "talk to the witch"){}
    bool triggerEvent(){
        string s;
        if(items[7].getExist()==1){
            cout << endl << "Witch : Hi! What do you want to do?" << endl
             << "A. become a wizard" << endl << "B. change my type" << endl << "C. go back to menu" << endl;
            cin >> s;
            if(s=="A"){
                cout << endl << "You have to exchange your sword and shield with wand and robe. Do you agree?" << endl << "A. agree" << endl << "B. go back to menu" << endl;
                cin >> s;
                if(s=="A"){
                    if(items[2].getDisappear()==1||items[2].getExist()==1){
                        cout << endl << "You don't have a shield." << endl;
                    }else if(items[5].getDisappear()==1||items[5].getExist()==1){
                        cout << endl << "You don't have a sword." << endl;
                    }else{
                        if(items[2].getWore()==1){
                            items[2].takeoff();
                        }
                        if(items[5].getWore()==1){
                            items[5].takeoff();
                        }
                        items[2].setDisappear(1);
                        items[5].setDisappear(1);
                        items[4].setExist(0);
                        items[7].setExist(0);
                        cout << endl << "You become a wizard. Try to put on your wand and robe." << endl;
                    }
                }else if(s!="B"){
                    cout << endl << "Error input!" << endl;
                }
            }else if(s=="B"){
                if(gem.getExist()==0){
                    cout << endl << "Which type?" << endl << "A. water" << endl << "B. fire" << endl << "C. grass" << endl;
                    cin >> s;
                    if(s=="A"){
                        play.setType(0);
                        cout << endl << "Your type have change into water." << endl;
                    }else if(s=="B"){
                        play.setType(1);
                        cout << endl << "Your type have change into fire." << endl;
                    }else if(s=="C"){
                        play.setType(1);
                        cout << endl << "Your type have change into grass." << endl;
                    }else{
                        cout << endl << "Error input!" << endl;
                    }
                }else{
                    cout << endl << "You don't have gem." << endl;
                }
            }else if(s!="C"){
                cout << endl << "Error input!" << endl;
            }
        }else{
            cout << endl << "Witch : Hi! What do you want to do?" << endl << "A. buy the spell book with 100 coins" << endl
             << "B. change my type" << endl << "C. go back to menu" << endl;
             cin >> s;
            if(s=="A"){
                if(items[8].getExist()==0){
                    cout << endl << "It sold out." << endl;
                }else if(play.getCoin()<100){
                    cout << endl << "You don't have 100 coins." << endl;
                }else{
                    items[8].setExist(0);
                    play.setCoin(play.getCoin()-100);
                    cout << endl << "You get the spell book." << endl;
                }
            }else if(s=="B"){
                if(gem.getExist()==0){
                    cout << endl << "Which type?" << endl << "A. water" << endl << "B. fire" << endl << "C. grass" << endl;
                    cin >> s;
                    if(s=="A"){
                        play.setType(0);
                        cout << endl << "Your type have change into water." << endl;
                    }else if(s=="B"){
                        play.setType(1);
                        cout << endl << "Your type have change into fire." << endl;
                    }else if(s=="C"){
                        play.setType(1);
                        cout << endl << "Your type have change into grass." << endl;
                    }else{
                        cout << endl << "Error input!" << endl;
                    }
                }else{
                    cout << endl << "You don't have gem." << endl;
                }
            }else if(s=="C"){
            }else{
                cout << endl << "Error input!" << endl;
            }
        }
    }
};

Witch witch;

class Merchant: public Object
{
private:
public:
    Merchant():Object("merchant", "talk to the merchant"){}
    bool triggerEvent(){
        string s;
        cout << endl << "Merchant : Hi! What do you want to do?" << endl << "A. buy the bulletproof shield with 100 coins" << endl
         << "B. buy the poison sword with 100 coins" << endl;
        if(items[2].getDisappear()==0&&items[2].getExist()==0){
            cout << "C. sell the shield for 50 coins" << endl << "D. go back to menu" << endl;
            cin >> s;
            if(s=="A"){
                if(items[3].getExist()==0){
                    cout << endl << "It sold out." << endl;
                }else if(play.getCoin()<100){
                    cout << endl << "You don't have 100 coins." << endl;
                }else{
                    items[3].setExist(0);
                    play.setCoin(play.getCoin()-100);
                    cout << endl << "You get the bulletproof shield." << endl;
                }
            }else if(s=="B"){
                if(items[6].getExist()==0){
                    cout << endl << "It sold out." << endl;
                }else if(play.getCoin()<100){
                    cout << endl << "You don't have 100 coins." << endl;
                }else{
                    items[6].setExist(0);
                    play.setCoin(play.getCoin()-100);
                    cout << endl << "You get the poison sword." << endl;
                }
            }else if(s=="C"){
                if(items[2].getWore()==1){
                    items[2].takeoff();
                }
                items[2].setDisappear(1);
                play.setCoin(play.getCoin()+50);
                cout << endl << "You get 50 coins." << endl;
            }else if(s!="D"){
                cout << endl << "Error input!" << endl;
            }
        }else{
            cout << "C. go back to menu" << endl;
            cin >> s;
            if(s=="A"){
                if(items[3].getExist()==0){
                    cout << endl << "It sold out." << endl;
                }else if(play.getCoin()<100){
                    cout << endl << "You don't have 100 coins." << endl;
                }else{
                    items[3].setExist(0);
                    play.setCoin(play.getCoin()-100);
                    cout << endl << "You get the bulletproof shield." << endl;
                }
            }else if(s=="B"){
                if(items[6].getExist()==0){
                    cout << endl << "It sold out." << endl;
                }else if(play.getCoin()<100){
                    cout << endl << "You don't have 100 coins." << endl;
                }else{
                    items[6].setExist(0);
                    play.setCoin(play.getCoin()-100);
                    cout << endl << "You get the poison sword." << endl;
                }
            }else if(s!="C"){
                cout << endl << "Error input!" << endl;
            }

        }
    }
};

Merchant merchant;

bool Monster::triggerEvent(){
    string s;
    while(1){
        cout << endl << "What do you want to do?" << endl << "A. attack" << endl;
        if(potions[0].getExist()==0&&potions[0].getUsed()==0){
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. use the potion" << endl << "D. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    potions[0].use();
                }else if(s=="D"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. use the potion" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    potions[0].use();
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }else if(potions[1].getExist()==0&&potions[1].getUsed()==0){
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. use the potion" << endl << "D. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    potions[1].use();
                }else if(s=="D"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. use the potion" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    potions[1].use();
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }else{
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }
        if(getCurrentHealth()<=0){
            cout << play.getName() << " beat the monster." << endl;
            if(play.getCurrentRoom()->getIndex1()==1||play.getCurrentRoom()->getIndex1()==2){
                rooms[1][4].allow(1,1,1,1);
                rooms[2][4].allow(1,1,1,1);
            }else{
                rooms[3][4].allow(1,1,1,1);
                rooms[4][4].allow(1,1,1,1);
            }
            setExist(0);
            break;
        }
        if(play.getCurrentHealth()<=0){
            cout << "You lose!" << endl;
            break;
        }
    }
}

void Monster::fight(){
    if(items[7].getWore()==1){
        cout  << endl<< play.getName() << "'s attack does " << play.getAttack()+typecounter() << " damage." << endl;
        setCurrentHealth(getCurrentHealth()-(play.getAttack()+typecounter()));
    }else{
        cout  << endl<< play.getName() << "'s attack does " << play.getAttack()-getDefense()+typecounter() << " damage." << endl;
        setCurrentHealth(getCurrentHealth()-(play.getAttack()-getDefense()+typecounter()));
    }
    if(getCurrentHealth()<=0){
        return;
    }
    if(getpoisoned()==1){
        cout << "Poison does 10 damage." << endl;
        setCurrentHealth(getCurrentHealth()-10);
    }
    if(getCurrentHealth()<=0){
        return;
    }
    cout << "Monster left " << getCurrentHealth() << " health." << endl;
    cout << "Monster's attack does " << getAttack()-play.getDefense()-typecounter() << " damage." << endl;
    play.setCurrentHealth(play.getCurrentHealth()-(getAttack()-play.getDefense()-typecounter()));
    if(play.getCurrentHealth()<=0){
        return;
    }
    cout <<  play.getName() << " left " << play.getCurrentHealth() << " health." << endl;
}

bool Boss::triggerEvent(){
    string s;
    while(1){
        cout << endl << "What do you want to do?" << endl << "A. attack" << endl;
        if(potions[0].getExist()==0&&potions[0].getUsed()==0){
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. use the potion" << endl << "D. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    potions[0].use();
                }else if(s=="D"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. use the potion" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    potions[0].use();
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }else if(potions[1].getExist()==0&&potions[1].getUsed()==0){
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. use the potion" << endl << "D. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    potions[1].use();
                }else if(s=="D"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. use the potion" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    potions[1].use();
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }else{
            if(poison.getExist()==0&&poison.getUsed()==0){
                cout << "B. use the poison" << endl << "C. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    setpoisoned(1);
                    poison.setUsed(1);
                    cout << endl << "You use the poison to the " << getName() << "." << endl;
                }else if(s=="C"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }else{
                cout << "B. retreat" << endl;
                cin >> s;
                if(s=="A"){
                    fight();
                }else if(s=="B"){
                    break;
                }else{
                    cout << "Error input!" << endl;
                }
            }
        }
        if(getCurrentHealth()<=0){
            cout << play.getName() << " beat the boss" << endl << endl << "You win! Congratulation!" << endl;
            setExist(0);
            break;
        }
        if(play.getCurrentHealth()<=0){
            cout << "You lose!" << endl;
            break;
        }
    }
}

void Boss::fight(){
    if(items[7].getWore()==1){
        cout  << endl<< play.getName() << "'s attack does " << play.getAttack()+typecounter() << " damage." << endl;
        setCurrentHealth(getCurrentHealth()-(play.getAttack()+typecounter()));
    }else{
        cout  << endl<< play.getName() << "'s attack does " << play.getAttack()-getDefense()+typecounter() << " damage." << endl;
        setCurrentHealth(getCurrentHealth()-(play.getAttack()-getDefense()+typecounter()));
    }
    if(getCurrentHealth()<=0){
        return;
    }
    if(getpoisoned()==1){
        cout << "Poison does 10 damage." << endl;
        setCurrentHealth(getCurrentHealth()-10);
    }
    if(getCurrentHealth()<=0){
        return;
    }
    cout << "Boss left " << getCurrentHealth() << " health." << endl;
    cout << "Boss's attack does " << getAttack()-play.getDefense()-typecounter() << " damage." << endl;
    play.setCurrentHealth(play.getCurrentHealth()-(getAttack()-play.getDefense()-typecounter()));
    if(play.getCurrentHealth()<=0){
        return;
    }
    cout <<  play.getName() << " left " << play.getCurrentHealth() << " health." << endl;
}

Object noneobject("","");
Item noneitem("","",0,0,0);

void Gamestart(){
    noneobject.setExist(0);
    noneitem.setWore(0);
    for(int i=0;i<6;i++){
        rooms[i][0].setDownRoom(&rooms[i][4]);
        rooms[i][1].setUpRoom(&rooms[i][4]);
        rooms[i][2].setRightRoom(&rooms[i][4]);
        rooms[i][3].setLeftRoom(&rooms[i][4]);
        rooms[i][4].setUpRoom(&rooms[i][0]);
        rooms[i][4].setDownRoom(&rooms[i][1]);
        rooms[i][4].setLeftRoom(&rooms[i][2]);
        rooms[i][4].setRightRoom(&rooms[i][3]);
        rooms[i][0].setObject1(&noneobject);
        rooms[i][0].setObject2(&noneobject);
        rooms[i][1].setObject1(&noneobject);
        rooms[i][1].setObject2(&noneobject);
        rooms[i][2].setObject1(&noneobject);
        rooms[i][2].setObject2(&noneobject);
        rooms[i][3].setObject1(&noneobject);
        rooms[i][3].setObject2(&noneobject);
        rooms[i][4].setObject1(&noneobject);
        rooms[i][4].setObject2(&noneobject);
    }
    for(int i=0;i<9;i++){
        items[i].setsamepart1(&noneitem);
        items[i].setsamepart2(&noneitem);
    }
    rooms[0][3].setUpRoom(&rooms[1][2]);
    rooms[0][3].setDownRoom(&rooms[2][2]);
    rooms[1][2].setLeftRoom(&rooms[0][3]);
    rooms[1][3].setRightRoom(&rooms[3][2]);
    rooms[1][3].setDownRoom(&rooms[4][2]);
    rooms[2][2].setLeftRoom(&rooms[0][3]);
    rooms[2][3].setUpRoom(&rooms[3][2]);
    rooms[2][3].setRightRoom(&rooms[4][2]);
    rooms[3][2].setLeftRoom(&rooms[1][3]);
    rooms[3][2].setDownRoom(&rooms[2][3]);
    rooms[3][3].setRightRoom(&rooms[5][2]);
    rooms[4][2].setUpRoom(&rooms[1][2]);
    rooms[4][2].setLeftRoom(&rooms[2][3]);
    rooms[4][3].setRightRoom(&rooms[5][2]);
    rooms[5][2].setUpRoom(&rooms[3][3]);
    rooms[5][2].setDownRoom(&rooms[4][3]);
    rooms[0][0].setObject1(&items[1]);
    rooms[0][2].setObject1(&items[2]);
    rooms[0][2].setObject2(&items[5]);
    rooms[0][1].setObject1(&items[0]);
    rooms[1][0].setObject1(&coins1);
    rooms[2][0].setObject1(&coins2);
    rooms[3][0].setObject1(&coins3);
    rooms[4][0].setObject1(&gem);
    rooms[1][4].setObject1(&monster1);
    rooms[2][4].setObject1(&monster1);
    rooms[3][4].setObject1(&monster2);
    rooms[4][4].setObject1(&monster2);
    rooms[3][4].setObject2(&girl);
    rooms[4][4].setObject2(&girl);
    rooms[1][1].setObject1(&key);
    rooms[2][1].setObject1(&key);
    rooms[3][1].setObject1(&merchant);
    rooms[4][1].setObject1(&witch);
    rooms[5][0].setObject1(&potions[0]);
    rooms[5][1].setObject1(&potions[1]);
    rooms[5][2].setObject1(&lock);
    rooms[5][3].setObject1(&poison);
    rooms[5][4].setObject1(&boss);
    items[0].setsamepart1(&items[4]);
    items[1].setsamepart1(&items[4]);
    items[2].setsamepart1(&items[3]);
    items[2].setsamepart2(&items[8]);
    items[3].setsamepart1(&items[2]);
    items[3].setsamepart2(&items[8]);
    items[4].setsamepart1(&items[0]);
    items[4].setsamepart2(&items[1]);
    items[5].setsamepart1(&items[6]);
    items[5].setsamepart2(&items[7]);
    items[6].setsamepart1(&items[5]);
    items[6].setsamepart2(&items[7]);
    items[7].setsamepart1(&items[5]);
    items[7].setsamepart2(&items[6]);
    items[8].setsamepart1(&items[2]);
    items[8].setsamepart2(&items[3]);
    cout << "Game Intro:" << endl << "1. type : water > fire > grass > water" << endl << "2. Magic attack can ignore the defense." << endl;
}

void Gamerestart(){
    int i;
    string s;
    cout << endl << "Please enter your name : ";
    cin >> s;
    cout << "Your name is " << s << "." << endl;
    play.setAttack(15);
    play.setCoin(0);
    play.setCurrentHealth(100);
    play.setCurrentRoom(&rooms[0][4]);
    play.setDefense(0);
    play.setMaxHealth(100);
    play.setName(s);
    s="";
    while(s!="A"&&s!="B"&&s!="C"){
        cout << endl << "Which type do you want to be?" << endl << "A. water" << endl << "B. fire" << endl << "C. grass" << endl;
        cin >> s;
        if(s=="A"){
            cout << "Your type is water. Unfortunately, you enter the grass dungeon." << endl;
            play.setType(0);
            monster1.setType(2);
            monster2.setType(2);
            boss.setType(2);
        }else if(s=="B"){
            cout << "Your type is fire. Unfortunately, you enter the water dungeon." << endl;
            play.setType(1);
            monster1.setType(0);
            monster2.setType(0);
            boss.setType(0);
        }else if(s=="C"){
            cout << "Your type is grass. Unfortunately, you enter the fire dungeon." << endl;
            play.setType(2);
            monster1.setType(1);
            monster2.setType(1);
            boss.setType(1);
        }else{
            cout << "Error input!" << endl;
        }
    }
    for(i=0;i<9;i++){
        items[i].setDisappear(0);
        items[i].setExist(1);
        items[i].setWore(0);
    }
    monster1.setCurrentHealth(50);
    monster1.setExist(1);
    monster1.setpoisoned(0);
    monster2.setCurrentHealth(50);
    monster2.setExist(0);
    monster2.setpoisoned(0);
    boss.setCurrentHealth(100);
    boss.setExist(1);
    boss.setpoisoned(0);
    coins1.setExist(1);
    coins2.setExist(1);
    coins3.setExist(1);
    for(i=1;i<5;i++){
        rooms[i][4].allow(0,0,1,0);
    }
    rooms[5][2].allow(1,1,0,0);
    gem.setExist(1);
    key.setExist(1);
    lock.setExist(1);
    girl.setExist(1);
}

void Gameloadstart(){
    int i,j,k;
    bool b0,b1,b2,b3;
    string s;
    fstream filedata("data.txt");
    filedata >> i >> j>> k;
    play.setAttack(i);
    play.setCoin(j);
    play.setCurrentHealth(k);
    filedata >> i >> j;
    play.setCurrentRoom(&rooms[i][j]);
    filedata >> i >> j;
    play.setDefense(i);
    play.setMaxHealth(j);
    filedata >> s;
    play.setName(s);
    filedata >> i >> j;
    play.setType(i);
    monster1.setType(j);
    monster2.setType(j);
    boss.setType(j);
    for(i=0;i<9;i++){
        filedata >> b0 >> b1 >> b2;
        items[i].setDisappear(b0);
        items[i].setExist(b1);
        items[i].setWore(b2);
    }
    filedata >> i >> j >> k;
    monster1.setCurrentHealth(i);
    monster1.setExist(j);
    monster1.setpoisoned(k);
    filedata >> i >> j >> k;
    monster2.setCurrentHealth(i);
    monster2.setExist(j);
    monster2.setpoisoned(k);
    filedata >> i >> j >> k;
    boss.setCurrentHealth(i);
    boss.setExist(j);
    boss.setpoisoned(k);
    filedata >> i >> j >> k;
    coins1.setExist(i);
    coins2.setExist(j);
    coins3.setExist(k);
    for(i=1;i<5;i++){
        filedata >> b0 >> b1 >> b2 >> b3;
        rooms[i][4].allow(b0,b1,b2,b3);
    }
    filedata >> b0 >> b1 >> b2 >> b3;
    rooms[5][2].allow(b0,b1,b2,b3);
    filedata >> i >> j >> k;
    gem.setExist(i);
    key.setExist(j);
    lock.setExist(k);
    filedata >> i;
    girl.setExist(i);
    filedata.close();
}

void Gamesavedata(){
    int i;
    fstream filedata("data.txt");
    filedata << play.getAttack() << endl << play.getCoin() << endl << play.getCurrentHealth() << endl;
    filedata << play.getCurrentRoom()->getIndex1() << endl << play.getCurrentRoom()->getIndex2() << endl;
    filedata << play.getDefense() << endl << play.getMaxHealth() << endl << play.getName() << endl << play.getType() << endl << monster1.getType() << endl;
    for(i=0;i<9;i++){
        filedata << items[i].getDisappear() << endl << items[i].getExist() << endl << items[i].getWore() << endl;
    }
    filedata << monster1.getCurrentHealth() << endl << monster1.getExist() << endl << monster1.getpoisoned() << endl;
    filedata << monster2.getCurrentHealth() << endl << monster2.getExist() << endl << monster2.getpoisoned() << endl;
    filedata << boss.getCurrentHealth() << endl << boss.getExist() << endl << boss.getpoisoned() << endl;
    filedata << coins1.getExist() << endl << coins2.getExist() << endl << coins3.getExist() << endl;
    for(i=1;i<5;i++){
        filedata << rooms[i][4].getallowup() << endl << rooms[i][4].getallowdown() << endl << rooms[i][4].getallowleft() << endl << rooms[i][4].getallowright() <<endl;
    }
    filedata << rooms[5][2].getallowup() << endl << rooms[5][2].getallowdown() << endl << rooms[5][2].getallowleft() << endl << rooms[5][2].getallowright() <<endl;
    filedata << gem.getExist() << endl << key.getExist() << endl << lock.getExist() << endl << girl.getExist() << endl;
    filedata.close();
}

void Room::menu(){
    int i;
    string s,t;
    cout << endl << "You are in Room " << play.getCurrentRoom()->getIndex1() << " zone " << play.getCurrentRoom()->getIndex2()+1 << "." << endl;
    cout << "What do you want to do?" << endl << "A. move" << endl << "B. show status" << endl << "C. open backpack" << endl;
    if(getobject1exist()==1&&getObject1()->getExist()==1){
        if(getobject2exist()==1&&getObject2()->getExist()==1){
            cout << "D. " << getObject1()->getScript() << endl << "E. " << getObject2()->getScript() << endl;
        }else{
            cout << "D. " << getObject1()->getScript() << endl;
        }
    }else if(getobject2exist()==1&&getObject2()->getExist()==1){
        cout << "D. " << getObject2()->getScript() << endl;
    }
    cout << "Z. leave the game" << endl;
    cin >> s;
    if(s=="A"){
        t="A. ";
        cout << endl << "Where do you want to go?" << endl;
        if(getallowup()){
            if(getIndex1()==getUpRoom()->getIndex1()){
                cout << t << "go up" << endl;
            }else{
                cout << t << "go to Room " << getUpRoom()->getIndex1() << endl;
            }
            t[0]++;
        }
        if(getallowdown()){
            if(getIndex1()==getDownRoom()->getIndex1()){
                cout << t << "go down" << endl;
            }else{
                cout << t << "go to Room " << getDownRoom()->getIndex1() << endl;
            }
            t[0]++;
        }
        if(getallowleft()){
            if(getIndex1()==getLeftRoom()->getIndex1()){
                cout << t << "go left" << endl;
            }else{
                cout << t << "go to Room " << getLeftRoom()->getIndex1() << endl;
            }
            t[0]++;
        }
        if(getallowright()){
            if(getIndex1()==getRightRoom()->getIndex1()){
                cout << t << "go right" << endl;
            }else{
                cout << t << "go to Room " << getRightRoom()->getIndex1() << endl;
            }
            t[0]++;
        }
        cin >> s;
        t="A";
        if(getallowup()){
            if(s==t){
                play.setCurrentRoom(getUpRoom());
            }
            t[0]++;
        }
        if(getallowdown()){
            if(s==t){
                play.setCurrentRoom(getDownRoom());
            }
            t[0]++;
        }
        if(getallowleft()){
            if(s==t){
                play.setCurrentRoom(getLeftRoom());
            }
            t[0]++;
        }
        if(getallowright()){
            if(s==t){
                play.setCurrentRoom(getRightRoom());
            }
            t[0]++;
        }
    }else if(s=="B"){
        cout << endl << "Name    : " << play.getName() << endl;
        cout << "Health  : " << play.getCurrentHealth() << "/" << play.getMaxHealth() << endl;
        cout << "Attack  : " << play.getAttack() << endl;
        cout << "Defense : " << play.getDefense() << endl;
        cout << "Coin    : " << play.getCoin() << endl;
        cout << "Type    : " << play.getTypename() << endl;
        cout << "Equiped : ";
        for(i=0;i<9;i++){
            if(items[i].getDisappear()==0&&items[i].getWore()==1){
                cout << items[i].getName();
                i++;
                break;
            }
        }
        for(i;i<9;i++){
            if(items[i].getDisappear()==0&&items[i].getWore()==1){
                cout << ", " << items[i].getName();
            }
        }
        cout << endl;
    }else if(s=="C"){
        cout << endl << "What do you want to see?" << endl << "A. equipment" << endl << "B. potion" << endl << "C. key" << endl << "D. gem" << endl;
        cin >> s;
        if(s=="A"){
            t="A. ";
            for(i=0;i<9;i++){
                if(items[i].getDisappear()==0&&items[i].getExist()==0&&items[i].getWore()==0){
                    t="B. ";
                    break;
                }
            }
            if(t=="A. "){
                cout << "It's empty." << endl;
            }else{
                t="A. ";
                cout << endl << "What do you want to put on?" << endl;
                for(i=0;i<9;i++){
                    if(items[i].getDisappear()==0&&items[i].getExist()==0&&items[i].getWore()==0){
                        cout << t << items[i].getName() << endl;
                        t[0]++;
                    }
                }
                if(t!="A. "){
                    cin >> s;
                    t="A";
                    for(i=0;i<9;i++){
                        if(items[i].getDisappear()==0&&items[i].getExist()==0&&items[i].getWore()==0){
                            if(s==t){
                                items[i].wear();
                                break;
                            }
                            t[0]++;
                        }
                    }
                }
            }
        }else if(s=="B"){
            if((potions[0].getExist()==0&&potions[0].getUsed()==0)||(potions[1].getExist()==0&&potions[1].getUsed()==0)||(poison.getExist()==0&&poison.getUsed()==0)){
                cout << "You have ";
                if((potions[0].getExist()==0&&potions[0].getUsed()==0)&&(potions[1].getExist()==0&&potions[1].getUsed()==0)){
                    if(poison.getExist()==0&&poison.getUsed()==0){
                        cout << "two potions and a poison." <<endl;
                    }else{
                        cout << "two potions." <<endl;
                    }
                }else if((potions[0].getExist()==0&&potions[0].getUsed()==0)||(potions[1].getExist()==0&&potions[1].getUsed()==0)){
                    if(poison.getExist()==0&&poison.getUsed()==0){
                        cout << "a potion and a poison." <<endl;
                    }else{
                        cout << "a potion." <<endl;
                    }
                }else{
                    cout << "a poison." <<endl;
                }
            }else{
                cout << "It's empty." << endl;
            }
        }else if(s=="C"){
            if(key.getExist()==0){
                cout << "You have a key." << endl;
            }else{
                cout << "It's empty." << endl;
            }
        }else if(s=="D"){
            if(gem.getExist()==0){
                cout << "You have a gem." << endl;
            }else{
                cout << "It's empty." << endl;
            }
        }else{
            cout << "Error Input!" << endl;
        }

    }else if(s=="D"&&getobject1exist()==1&&getObject1()->getExist()){
        getObject1()->triggerEvent();
    }else if(s=="D"&&getobject2exist()==1&&getObject2()->getExist()){
        getObject2()->triggerEvent();
    }else if(s=="E"&&getobject2exist()==1&&getObject2()->getExist()){
        getObject2()->triggerEvent();
    }else if(s=="Z"){
        return;
    }else{
        cout << "Error input!" << endl;
    }
    if(play.getCurrentHealth()<=0){
        gameover=1;
        return;
    }
    if(boss.getCurrentHealth()<=0){
        gameover=1;
        return;
    }
    play.getCurrentRoom()->menu();
}

int main(){
    string s="A";
    Gamestart();
    while(s!="Z"){
        gameover=0;
        s="";
        while(1){
            cout << endl << "Start a new game or Load previous data?" << endl << "A. start a new game" << endl << "B. load previous data" << endl << "Z. leave the game" << endl;
            cin >> s;
            if(s=="A"||s=="B"||s=="Z"){
                break;
            }else{
                cout << "Error input!" << endl;
            }
        }
        if(s=="A"){
            Gamerestart();
        }else if(s=="B"){
            Gameloadstart();
        }else{
            break;
        }
        play.getCurrentRoom()->menu();
        if(gameover==0){
            while(1){
                cout << "Do you want to save the data?" << endl << "A. yes" << endl << "B. no" << endl;
                cin >> s;
                if(s=="A"){
                    s="Z";
                    Gamesavedata();
                    break;
                }else if(s=="B"){
                    s="Z";
                    break;
                }
            }
        }
    }
    return 0;
}
