from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter,Depends,HTTPException,status,Response,Request
from sqlalchemy.orm import Session
from .. import schemas,database,oauth2,model

router = APIRouter(prefix="/vote", tags= ["vote"])

@router.post("/", status_code= status.HTTP_201_CREATED,response_model= schemas.VoteRes)
def vote(payload:schemas.Vote, db: Session = Depends(database.get_db),
         current_user:schemas.CreateUser = Depends(oauth2.get_current_user)):
    # query get vote from tbl_vote
    get_vote_query = db.query(model.Vote).filter(
        model.Vote.int_post_id == payload.int_post_id,model.Vote.int_user_id == current_user.int_user_id
        )
    
    vote = get_vote_query.first()
    
    if payload.dir == 1:
        # in case of already voted then throw exception
        if vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= f"user {current_user.vchr_email} has already voted on {vote.int_post_id}" )
        # adding new vote
        try:
            new_vote = model.Vote(int_post_id = payload.int_post_id,int_user_id= current_user.int_user_id)
            db.add(new_vote)
            db.commit()
        # if user enter a incorrect post id then handle exception
        except IntegrityError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with {payload.int_post_id} doesn't exist")
        return {"str_message": "SUCCESSFULLY_ADDED_VOTE"}
    else:
        # in case of unlike if already not voted then handle exception
        if not vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote doest not exist")
        
        get_vote_query.delete(synchronize_session=False)
        db.commit()
        return {"str_message": "SUCCESSFULLY_DELETED_VOTE"}
        
        