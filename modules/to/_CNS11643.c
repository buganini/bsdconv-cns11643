#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <bsdconv.h>

int cbcreate(struct bsdconv_instance *ins, struct bsdconv_hash_entry *arg){
	THIS_CODEC(ins)->priv=bsdconv_create("CNS11643");
	return 0;
}

void cbdestroy(struct bsdconv_instance *ins){
	void *p=THIS_CODEC(ins)->priv;
	bsdconv_destroy(p);
}

void cbconv(struct bsdconv_instance *ins){
	char *data;
	struct bsdconv_phase *this_phase=THIS_PHASE(ins);
	struct bsdconv_instance *cns=THIS_CODEC(ins)->priv;
	struct data_rt *data_p=this_phase->curr;
	data=this_phase->curr->data;

	/* exclude ASCII*/
	if(ins->phase[ins->phase_index].curr->len==2 && (data[1] & bb10000000)==0){
		this_phase->state.status=DEADEND;
		return;
	}

	switch(*data){
		case 0x01:
			if(cns!=NULL){
				bsdconv_init(cns);
				cns->input.data=data;
				cns->input.len=this_phase->curr->len;
				cns->input.flags=0;
				cns->input.next=NULL;
				cns->flush=1;
				bsdconv(cns);
				data_p=cns->phase[cns->phasen].data_head->next;
				cns->phase[cns->phasen].data_head->next=NULL;
				data=data_p->data;
			}
			if(*data==0x02){
				goto converted;
			}else{
				this_phase->state.status=DEADEND;
				if(data_p!=this_phase->curr)
					DATUM_FREE(ins, data_p);
				return;
			}
		case 0x02:
			converted:

			DATA_MALLOC(ins, this_phase->data_tail->next);
			this_phase->data_tail=this_phase->data_tail->next;
			this_phase->data_tail->next=NULL;

			this_phase->data_tail->flags=F_FREE;
			this_phase->data_tail->len=4;
			this_phase->data_tail->data=malloc(4);
			memcpy(this_phase->data_tail->data, data, this_phase->data_tail->len);
			CP(this_phase->data_tail->data)[0]=0;
			this_phase->state.status=NEXTPHASE;

			if(data_p!=this_phase->curr)
				DATUM_FREE(ins, data_p);

			return;
		default:
			this_phase->state.status=DEADEND;
			return;
	}
}
