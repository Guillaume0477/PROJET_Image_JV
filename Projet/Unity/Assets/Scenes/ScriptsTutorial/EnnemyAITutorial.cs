using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAITutorial : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public PlayerStatsTutorial Target;
    public EnnemyStatsTutorial ennemyStats;
    public EnnemyBarTutorial ennemyBar;

    private float Distance;
    private float ennemy_speed = 5;
    private float attackRange = 2.2f;
    private float attackRepeatTime = 1;
    private float Damping = 6;
    private float TheDammage = 0;
    private Animator anim;
    private bool isAttacked;
    private bool isDead;

	// At the start of the game..
	void Start ()
	{
        ennemyBar.SetMaxValue(ennemyStats.getHealth());
        anim = GetComponent<Animator>();
    }

	// Each physics step..
	void Update ()
	{
        Distance = Vector3.Distance(Target.transform.position, transform.position);

        lookAt();
        setHealthBar();

        if (ennemyStats.getHealth() > 0)
        {
            if ((!isAttacked) && (!ennemyStats.getIsTouched()))
            {
                if(Distance < attackRange)
                {
                    StartCoroutine("attack");
                }
                else{
                    chase();
                }
            }
        }
        else
        {
            if(!isDead)
            {
                Dead();
            }
        }
    }

    void chase()
    {
        anim.Play("Base Layer.Run In Place");
        transform.position = Vector3.MoveTowards(transform.position, Target.transform.position, ennemy_speed * Time.deltaTime);
    }

    void lookAt()
    {
        Quaternion rotation = Quaternion.LookRotation(Target.transform.position - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, rotation, Time.deltaTime * Damping);
    }

    IEnumerator attack()
    {
        isAttacked = true;
        anim.Play("Base Layer.Attack 01");
        Target.ApplyDammage(TheDammage);
        yield return new WaitForSeconds(attackRepeatTime);
        isAttacked = false;
    }

    void Dead()
	{
        isDead = true;

        Destroy(ennemyBar);
        anim.Play("Base Layer.Die");
		Destroy(gameObject, 3.0f);
	}

    void setHealthBar(){
        ennemyBar.SetValue(ennemyStats.getHealth());
    }

    public bool getIsDead()
    {
        return(isDead);
    }
}