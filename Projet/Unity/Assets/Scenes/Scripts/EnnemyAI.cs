using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAI : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public PlayerStats Target;
    public EnnemyStats ennemyStats;
    public EnnemyBar ennemyBar;

    private float Distance;
    private float attackTime = 1;
    private float ennemy_speed = 5;    
    private float attackRange = 2.2f;
    private float attackRepeatTime = 1;
    private float Damping = 6;
    private float TheDammage = 0;
    private Animator anim;

	// At the start of the game..
	void Start ()
	{
        attackTime = Time.time;
        ennemyBar.SetMaxValue(ennemyStats.getHealth());
        anim = GetComponent<Animator>();
    }

	// Each physics step..
	void Update ()
	{
        Distance = Vector3.Distance(Target.transform.position, transform.position);

        lookAt();
        setHealthBar();

        if(ennemyStats.getHealth() > 0)
        {
            if(Distance < attackRange){
                StartCoroutine("attack");
            }
            else{
                chase();
            }
        }
        else
        {
            Dead();
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
        if (Time.time > attackTime){
            anim.Play("Base Layer.Attack 01");
            // controller.Stop();
            Target.ApplyDammage(TheDammage);
            attackTime = Time.time + attackRepeatTime;
            // yield return new WaitForSeconds(anim.GetCurrentAnimatorStateInfo(0).length+anim.GetCurrentAnimatorStateInfo(0).normalizedTime);
            yield return new WaitForSeconds(5f);
        }
    }

    void Dead()
	{
        Destroy(ennemyBar);
        anim.Play("Base Layer.Die");
		Destroy (gameObject, 3.0f);
	}

    void setHealthBar(){
        ennemyBar.SetValue(ennemyStats.getHealth());
    }
}