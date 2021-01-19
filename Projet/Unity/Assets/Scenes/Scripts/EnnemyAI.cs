using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAI : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public PlayerStats Target;
    public EnnemyStats ennemyStats;
    public EnnemyBar ennemyBar;
    public Text count;
    public Text vague;

    private float Distance;
    private float ennemy_speed = 5;
    private float attackRange = 2.2f;
    private float attackRepeatTime = 1;
    private float Damping = 6;
    private float TheDammage = 0;
    private Animator anim;
    private bool isAttacked;
    private bool isDead;
    private bool isCount;

    ////////////////////////////////////// ATTENTION AU STATIC ! //////////////////////////////////////
    static private float count_death = 0;
    static private float count_vague = 1;
    static private float count_vague_series = 1;
    ////////////////////////////////////// ATTENTION AU STATIC ! //////////////////////////////////////

	// At the start of the game..
	void Start ()
	{
        ennemyBar.SetMaxValue(ennemyStats.getHealth() * count_vague_series);
        anim = GetComponent<Animator>();
        count.text = count_death.ToString();
        vague.text = count_vague.ToString();
    }

	// Each physics step..
	void Update ()
	{

        Debug.Log(ennemyStats.getHealth());

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

        count_death = count_death + 1;
        count.text = count_death.ToString();
        
        if (count_death % 1 == 0)
        {
            if (!isCount)
            {
                count_vague = (count_vague + 1);
                vague.text = count_vague.ToString();
                isCount = true;
            }
        }
        else
        {
            isCount = false;
        }

        if(count_vague % 2 == 0)
        {
            count_vague_series = count_vague_series + 1;
        }

        Destroy(ennemyBar);
        anim.Play("Base Layer.Die");
		Destroy(gameObject, 3.0f);
	}

    public float getCount_Series()
    {
        return(count_vague_series);
    }

    void setHealthBar(){
        ennemyBar.SetValue(ennemyStats.getHealth());
    }

    public bool getIsDead()
    {
        return(isDead);
    }
}