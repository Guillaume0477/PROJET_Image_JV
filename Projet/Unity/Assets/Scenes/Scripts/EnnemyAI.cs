using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAI : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public PlayerStats Target;
    public float ennemy_speed;    
    public float attackRange;
    public float attackRepeatTime;
    public int TheDammage;
    public float Damping;
    public EnnemyStats ennemyStats;
    public EnnemyBar ennemyBar;

    private float Distance;
    private float attackTime = 1;

	// At the start of the game..
	void Start ()
	{
        attackTime = Time.time;
        ennemyBar.SetMaxValue(ennemyStats.ennemyHealth);
    }

	// Each physics step..
	void Update ()
	{
        Distance = Vector3.Distance(Target.transform.position, transform.position);

        lookAt();
        setHealthBar();
        
        if(Distance < attackRange){
            attack();
        }

        else{
            chase();
        }
    }

    void chase()
    {
        transform.position = Vector3.MoveTowards(transform.position, Target.transform.position, ennemy_speed * Time.deltaTime);
    }

    void lookAt()
    {
        Quaternion rotation = Quaternion.LookRotation(Target.transform.position - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, rotation, Time.deltaTime * Damping);
    }

    void attack()
    {
        if (Time.time > attackTime){
            Target.ApplyDammage(TheDammage);
            attackTime = Time.time + attackRepeatTime;
        }
    }

    void setHealthBar(){
        ennemyBar.SetValue(ennemyStats.getHealth());
    }
}