using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyStats : MonoBehaviour 
{
	public EnnemyAI ennemyAI;

    private float ennemyHealth = 100;
	private Animator anim;
	private bool isTouched;

	void Start()
	{
		anim = GetComponent<Animator>();
		ennemyHealth = 100 * ennemyAI.getCount_Series();
	}
	
	void OnTriggerEnter (Collider col)
	{
        if(col.gameObject.tag == "Boule")
		{
			StartCoroutine("TakeDamageAnim");
            ennemyHealth -= 50; //col.gameObject.GetComponent<FireBall>().getEnnemyDamage() * 2.0f;
			Destroy(col.gameObject);
        }

		else if (col.gameObject.tag == "OndeChoc"){
			StartCoroutine("TakeDamageAnim");
            ennemyHealth -= col.gameObject.GetComponent<ShockWave>().getEnnemyDamage();	
		}
		
		else if (col.gameObject.tag == "Mine"){
			col.gameObject.transform.parent.GetComponent<Mine>().Explosion();
		}
    }

	void OnCollisionEnter (Collision col)
	{
		if(col.gameObject.tag == "Mine"){
			ennemyHealth -= col.gameObject.transform.parent.GetComponent<Mine>().getEnnemyDamage();
		}
	}

	IEnumerator TakeDamageAnim()
	{
		if(!ennemyAI.getIsDead())
		{
			isTouched = true;
			anim.Play("Base Layer.Take Damage");
			yield return new WaitForSeconds(0.5f);
			isTouched = false;
		}
	}

	public float getHealth ()
	{
		return(ennemyHealth);
    }

	public bool getIsTouched ()
	{
		return(isTouched);
    }
}