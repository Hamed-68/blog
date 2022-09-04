import { toast } from 'react-toastify';

const notify = (type, msg) => {
    if (type === 'success') {
        toast.success(msg);
    } else {
        toast.error(msg);
    }
};
export default notify;